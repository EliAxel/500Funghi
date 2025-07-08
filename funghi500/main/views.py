from django.shortcuts import redirect, render
from django.views.generic import TemplateView
import re
from .models import Fungo
from django.db.models import Q
# Create your views here.
import re

class ExprNode:
    def evaluate(self, values_set):
        raise NotImplementedError

class ValNode(ExprNode):
    def __init__(self, val):
        self.val = val

    def evaluate(self, values_set):
        return self.val in values_set

class NotNode(ExprNode):
    def __init__(self, child):
        self.child = child

    def evaluate(self, values_set):
        return not self.child.evaluate(values_set)

class AndNode(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, values_set):
        return self.left.evaluate(values_set) and self.right.evaluate(values_set)

class OrNode(ExprNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, values_set):
        return self.left.evaluate(values_set) or self.right.evaluate(values_set)

def loadcontext(context):
    rows = []
    context["months"] = [
        "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
        "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
    ]
    for i in range(10):
        row = []
        for j in range(10):
        # Calcola l'etichetta della cella
            label = 1 + j * 10 + i
            # Costruisci il nome file immagine (es: "img_1.png", "img_2.png", ...)
            image_name = f"img/funghi/{label}.png"
            row.append({'label': label, 'image': image_name})
        rows.append(row)
    context["rows"] = rows
    return context

def parse_expression(expr_str):
    token_pattern = re.compile(r'\s*(\d+|[!&|()])')
    tokens = token_pattern.findall(expr_str)

    def next_token():
        return tokens.pop(0) if tokens else None

    def peek_token():
        return tokens[0] if tokens else None

    def parse_atom():
        tok = next_token()
        if tok == '!':
            node = parse_atom()
            return NotNode(node)
        elif tok == '(':
            node = parse_or()
            if next_token() != ')':
                raise ValueError("Parentesi non chiusa")
            return node
        elif tok and tok.isdigit():
            return ValNode(int(tok))
        else:
            raise ValueError(f"Token inatteso: {tok}")

    def parse_and():
        node = parse_atom()
        while peek_token() == '&':
            next_token()  # consuma &
            right = parse_atom()
            node = AndNode(node, right)
        return node

    def parse_or():
        node = parse_and()
        while peek_token() == '|':
            next_token()  # consuma |
            right = parse_and()
            node = OrNode(node, right)
        return node

    tree = parse_or()

    if tokens:
        raise ValueError(f"Token residui non previsti: {tokens}")

    return tree

class MainPage(TemplateView):
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = loadcontext(context)
        return context
    
    def get(self, request):
        rgx = request.GET.get("q", "").strip()
        mesi = request.GET.get("mesi")
        diametro_min = request.GET.get("diametro_min")
        diametro_max = request.GET.get("diametro_max")
        altezza_min = request.GET.get("altezza_min")
        altezza_max = request.GET.get("altezza_max")
        altitudine_min = request.GET.get("altitudine_min")
        altitudine_max = request.GET.get("altitudine_max")
        expr = ""
        context = {}
        context = loadcontext(context)
        filtrati = Fungo.objects.all()
        
        # Filtro per espressione logica
        if rgx:
            if rgx == '':
                return render(request, self.template_name, context)
            
            pattern = r'^[0-9!&|()\s]+$'
            if not re.fullmatch(pattern, rgx):
                context["evento"] = "Formato ricerca non valido. Usa solo numeri, &, |, ! e parentesi."
                return render(request, self.template_name, context)

            try:
                expr_tree = parse_expression(rgx)
                tutti_funghi = Fungo.objects.prefetch_related('valori').all()
                ids_filtrati = []

                for f in tutti_funghi:
                    valori_set = set(f.valori.values_list('id', flat=True))
                    if expr_tree.evaluate(valori_set):
                        ids_filtrati.append(f.id) # type: ignore

                filtrati = filtrati.filter(id__in=ids_filtrati)
                context["mainexpr"] = rgx
            except Exception as e:
                print(f"Errore nel parsing dell'espressione: {str(e)}")
                context["evento"] = "Errore nell'interpretazione della ricerca"
                context["risultati"] = []
                context["num"] = 0
                return render(request, self.template_name, context)

        # Filtro per mesi
        if mesi:
            mesi_ids = [m.strip() for m in mesi.split(',') if m.strip()]
            if mesi_ids:
                # Filtra per i mesi selezionati (usando l'ID del mese)
                filtrati = filtrati.filter(mesi__id__in=mesi_ids).distinct()
                expr = expr + "mesi(" + mesi + ") "

        # Filtro per diametro (considerando sia MIN che MAX)
        if diametro_min:
            try:
                diametro_min = int(diametro_min)
                # Cerca funghi dove diametroMAX >= diametro_min (il fungo può arrivare almeno a questa dimensione)
                filtrati = filtrati.filter(diametroMAX__gte=diametro_min)
                expr = expr + "diaMIN(" + str(diametro_min) + "cm) "
            except ValueError:
                pass
                
        if diametro_max:
            try:
                diametro_max = int(diametro_max)
                # Cerca funghi dove diametroMIN <= diametro_max (il fungo parte almeno da questa dimensione)
                filtrati = filtrati.filter(diametroMIN__lte=diametro_max)
                expr = expr + "diaMAX(" + str(diametro_max) + "cm) "
            except ValueError:
                pass

        # Filtro per altezza (considerando sia MIN che MAX)
        if altezza_min:
            try:
                altezza_min = int(altezza_min)
                filtrati = filtrati.filter(altezzaMAX__gte=altezza_min)
                expr = expr + "altzMIN(" + str(altezza_min) + "cm) "
            except ValueError:
                pass
                
        if altezza_max:
            try:
                altezza_max = int(altezza_max)
                filtrati = filtrati.filter(altezzaMIN__lte=altezza_max)
                expr = expr + "altzMAX(" + str(altezza_max) + "cm) "
            except ValueError:
                pass

        # Filtro per altitudine (considerando sia MIN che MAX)
        if altitudine_min:
            try:
                altitudine_min = int(altitudine_min)
                filtrati = filtrati.filter(altitudineMAX__gte=altitudine_min)
                expr = expr + "altdnMIN(" + str(altitudine_min) + "m) "
            except ValueError:
                pass
                
        if altitudine_max:
            try:
                altitudine_max = int(altitudine_max)
                filtrati = filtrati.filter(altitudineMIN__lte=altitudine_max)
                expr = expr + "altdnMAX(" + str(altitudine_max) + "m)"
            except ValueError:
                pass
        
        if mesi or altezza_min or altezza_max or diametro_min or diametro_max or altitudine_min or altitudine_max or rgx:
            context["risultati"] = [f.id for f in filtrati] # type: ignore
            context["num"] = filtrati.count()
            
            # Mantieni i valori dei filtri nel contesto per mostrare i valori selezionati nel template
            context.update({
                "mesi_selezionati": mesi,
                "diametro_min": diametro_min,
                "diametro_max": diametro_max,
                "altezza_min": altezza_min,
                "altezza_max": altezza_max,
                "altitudine_min": altitudine_min,
                "altitudine_max": altitudine_max,
            })
            context["expr"] = expr
            
        return render(request, self.template_name, context)
        
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
        context = {}
        context = loadcontext(context)
        
        if rgx:
            # Regex semplificata per validazione
            pattern = r'^[0-9!&|()\s]+$'
            if not re.fullmatch(pattern, rgx):
                context["evento"] = "Formato ricerca non valido. Usa solo numeri, &, |, ! e parentesi."
                return render(request, self.template_name, context)

            try:
                expr_tree = parse_expression(rgx)
                tutti_funghi = Fungo.objects.prefetch_related('valori').all()
                filtrati = []

                for f in tutti_funghi:
                    valori_set = set(f.valori.values_list('id', flat=True))
                    if expr_tree.evaluate(valori_set):
                        filtrati.append(f)

                context["expr"] = rgx
                context["risultati"] = [f.id for f in filtrati]
                context["num"] = len(filtrati)
            except Exception as e:
                print(f"Errore nel parsing dell'espressione: {str(e)}")
                context["evento"] = "Errore nell'interpretazione della ricerca"
                context["risultati"] = []
                context["num"] = 0
            
            return render(request, self.template_name, context)
        
        return render(request, self.template_name, context)
        
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
# Create your views here.
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

class MainPage(TemplateView):
    template_name = 'main/main.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = loadcontext(context)
        context["risultati"] = [1,2,3,4,5,6,7]
        context["num"] = 7
        return context
    
    def post(self, request):
        rgx = request.POST.get("search-input")
        if rgx:
            
            context = {}
            context = loadcontext(context)
            return render(request, self.template_name, context)
        return render(request, self.template_name, {"ok": "onk"})
    
from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import fitimet, shpenzimet, totali
from .forms import fitimetForm, shpenzimetForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache
class LoginUserView(LoginView):
    template_name = 'registration/login.html'
@login_required
@never_cache
def shtepia(request):
    fitimet_totale = fitimet.objects.filter(user=request.user).aggregate(Sum('shuma'))['shuma__sum'] or 0
    shpenzimet_totale = shpenzimet.objects.filter(user=request.user).aggregate(Sum('shuma'))['shuma__sum'] or 0
    gjendja = fitimet_totale - shpenzimet_totale
    totali.objects.update_or_create(id=1, defaults={'fitimet_totale': fitimet_totale, 'shpenzimet_totale': shpenzimet_totale, 'gjendja': gjendja})
    return render(request, 'blog/shtepia.html', {'fitimet_totale': fitimet_totale, 'shpenzimet_totale': shpenzimet_totale, 'gjendja': gjendja})
@login_required
@never_cache
def fitimet_list(request):
    fitimet_list = fitimet.objects.filter(user=request.user)
    total=fitimet_list.aggregate(Sum('shuma'))['shuma__sum'] or 0
    return render(request, 'blog/fitimet_list.html', {'fitimet_list': fitimet_list})
class krijoardhuraCreateView(LoginRequiredMixin, CreateView):
    model = fitimet
    form_class = fitimetForm
    success_url = reverse_lazy('fitimet_list')
    template_name = 'blog/krijo_ardhura.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)
class MyLogoutView(LogoutView):
    http_method_names = ["get", "post"]    
class redaktoardhuraUpdateView(LoginRequiredMixin, UpdateView):
    model = fitimet
    form_class = fitimetForm
    template_name = 'blog/redakto_ardhura.html'
    success_url = reverse_lazy('fitimet_list')
class fshiardhuraDeleteView(LoginRequiredMixin, DeleteView):        
    model = fitimet
    template_name = 'blog/fshi_ardhura.html'
    success_url = reverse_lazy('fitimet_list')

@login_required
@never_cache
def shpenzimet_list(request):
    shpenzimet_list = shpenzimet.objects.filter(user=request.user)
    total=shpenzimet_list.aggregate(Sum('shuma'))['shuma__sum'] or 0
    return render(request, 'blog/shpenzimet_list.html', {'shpenzimet_list': shpenzimet_list, 'total': total})
class KrijoShpenzimeCreateView(LoginRequiredMixin, CreateView):
    model = shpenzimet
    form_class = shpenzimetForm
    success_url = reverse_lazy('shpenzimet_list')
    template_name = 'blog/krijo_shpenzime.html'


    def form_valid(self, form):
        shpenzim = form.save(commit=False)
        shpenzim.user = self.request.user
        shpenzim.save()
        return super().form_valid(form)
class RedaktoShpenzimeUpdateView(LoginRequiredMixin, UpdateView):
    model = shpenzimet
    form_class = shpenzimetForm
    template_name = 'blog/redakto_shpenzime.html'
    success_url = reverse_lazy('shpenzimet_list')
class FshiShpenzimeDeleteView(LoginRequiredMixin, DeleteView):
    model = shpenzimet
    template_name = 'blog/fshi_shpenzime.html'
    success_url = reverse_lazy('shpenzimet_list')
@login_required

def statistikat(request):
    viti = request.GET.get('viti')

    # FILTERS BASE
    fitimet_qs = fitimet.objects.filter(user=request.user)
    shpenzimet_qs = shpenzimet.objects.filter(user=request.user)

    if viti:
        viti = int(viti)
        fitimet_qs = fitimet_qs.filter(data__year=viti)
        shpenzimet_qs = shpenzimet_qs.filter(data__year=viti)

    # TOTALS
    fitimet_totale = fitimet_qs.aggregate(Sum('shuma'))['shuma__sum'] or 0
    shpenzimet_totale = shpenzimet_qs.aggregate(Sum('shuma'))['shuma__sum'] or 0

    gjendja = fitimet_totale - shpenzimet_totale

    # SHPENZIME SIPAS KATEGORIVE
    shpenzime_kat = (
        shpenzimet_qs
        .values("kategoria")
        .annotate(total=Sum("shuma"))
    )

    labels_shpenzime = [x["kategoria"] for x in shpenzime_kat] or []
    totale_shpenzime = [float(x["total"]) for x in shpenzime_kat] or []

    # FITIME SIPAS KATEGORIVE
    fitime_kat = (
        fitimet_qs
        .values("kategoria")
        .annotate(total=Sum("shuma"))
    )

    labels_fitime = [x["kategoria"] for x in fitime_kat] or []
    totale_fitime = [float(x["total"]) for x in fitime_kat] or []

    context = {
        "viti": viti,
        "fitimet_totale": fitimet_totale,
        "shpenzimet_totale": shpenzimet_totale,
        "gjendja": gjendja,

        "labels_shpenzime": labels_shpenzime,
        "totale_shpenzime": totale_shpenzime,

        "labels_fitime": labels_fitime,
        "totale_fitime": totale_fitime,

        "vitet": [2025, 2026, 2027],
    }

    return render(request, "blog/statistikat.html", context)
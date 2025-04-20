from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from .models import Newspaper, Redactor, Topic
from .forms import (
    NewspaperForm,
    RedactorCreationForm,
    RedactorUpdateForm,
    TopicForm,
    NewspaperSearchForm,
    RedactorSearchForm,
    TopicSearchForm,
)


class IndexView(generic.TemplateView):
    template_name = "newspaper/index.html"

    def get_context_data(self: Any, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context["num_newspapers"] = Newspaper.objects.count()
        context["num_redactors"] = Redactor.objects.count()
        context["num_topics"] = Topic.objects.count()
        return context


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 5
    template_name = "newspaper/newspaper_list.html"

    def get_context_data(self: Any, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        topic_id = self.request.GET.get("topic")
        context["search_form"] = NewspaperSearchForm(
            initial={"title": title, "topic": topic_id}
        )
        return context

    def get_queryset(self: Any) -> Any:
        queryset = Newspaper.objects.select_related("topic").prefetch_related(
            "publishers"
        )
        title = self.request.GET.get("title")
        topic_id = self.request.GET.get("topic")

        if title:
            queryset = queryset.filter(
                Q(title__icontains=title) | Q(content__icontains=title)
            )
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)

        return queryset


class NewspaperDetailView(generic.DetailView):
    model = Newspaper
    template_name = "newspaper/newspaper_detail.html"


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "newspaper/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "newspaper/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    template_name = "newspaper/newspaper_confirm_delete.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class TopicListView(generic.ListView):
    model = Topic
    paginate_by = 5
    template_name = "newspaper/topic_list.html"

    def get_context_data(self: Any, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TopicSearchForm(initial={"name": name})
        return context

    def get_queryset(self: Any) -> Any:
        queryset = Topic.objects.prefetch_related("newspapers")
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    form_class = TopicForm
    template_name = "newspaper/topic_form.html"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "newspaper/topic_form.html"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    template_name = "newspaper/topic_confirm_delete.html"
    success_url = reverse_lazy("newspaper:topic-list")


class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 5
    template_name = "newspaper/redactor_list.html"

    def get_context_data(self: Any, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        years = self.request.GET.get("years", "")
        context["search_form"] = RedactorSearchForm(
            initial={"username": username, "years": years}
        )
        return context

    def get_queryset(self: Any) -> Any:
        queryset = Redactor.objects.all()
        username = self.request.GET.get("username")
        years = self.request.GET.get("years")

        if username:
            queryset = queryset.filter(username__icontains=username)
        if years:
            queryset = queryset.filter(years_of_experience=years)

        return queryset


class RedactorDetailView(generic.DetailView):
    model = Redactor
    template_name = "newspaper/redactor_detail.html"


class RedactorCreateView(generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    template_name = "newspaper/redactor_form.html"
    success_url = reverse_lazy("newspaper:redactor-list")


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm
    template_name = "newspaper/redactor_form.html"
    success_url = reverse_lazy("newspaper:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    template_name = "newspaper/redactor_confirm_delete.html"
    success_url = reverse_lazy("newspaper:redactor-list")

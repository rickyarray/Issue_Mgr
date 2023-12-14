from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from .models import Issue, Status
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class BoardView(ListView):
    template_name = "issues/board.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_do = Status.objects.get(name="to do")
        in_prog = Status.objects.get(name="in progress")
        done = Status.objects.get(name="done")
        context["to_do_list"] = Issue.objects.filter(
            status=to_do
        ).order_by("created_on").reverse()
        context["in_prog_list"] = Issue.objects.filter(
            status=in_prog
        ).order_by("created_on").reverse()
        context["done_list"] = Issue.objects.filter(
            status=done
        ).order_by("created_on").reverse()
        return context


class StatusUpdateView(UpdateView):
    template_name = "issues/board.html"
    model = Issue
    fields = ["summary", "description", "status"]
    success_url = reverse_lazy("board")

    def form_valid(self, form):
        form.instance.status = Status.objects.get(name=form.instance.status)
        return super().form_valid(form)


class IssueDetailView(DetailView):
    template_name = "issues/detail.html"
    model = Issue

class IssueCreateView(LoginRequiredMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["summary", "description", "status"]

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)

class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ["summary", "description", "status"]

    def test_func(self):
        # This MUST return True or False
        issue = self.get_object()
        return issue.reporter == self.request.user

class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("board")

    def test_func(self):
        issue = self.get_object()
        return issue.reporter == self.request.user



# class TaskListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
#     template_name = "issues/board.html"
#     model = Issue

#     def get_context_data(self, **kwarg):
#         context = super().get_context_data(**kwarg)


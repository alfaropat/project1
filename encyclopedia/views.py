from django.shortcuts import render

from . import util
from django import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def add(request):
    if request.method == "POST":

        form = NewEntryForm(request.POST)

        if form.is_valid():
            entry_name = form.cleaned_data["entry_name"]
            entry_info = form.cleaned_data["entry_info"]

            util.save_entry(entry_name,entry_info)

            return render(request, "encyclopedia/entry.html", {
                "entry_name": entry_name,
                "entry_info": entry_info
            })

    return render(request, "encyclopedia/add.html", {
        "form_name": NewEntryForm(),
        "form_info": NewEntryForm()
    })

class NewEntryForm():
    entry = forms.CharField(label="New Entry")

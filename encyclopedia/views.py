from django.shortcuts import render

from markdown2 import markdown
from random import choice

from . import util

# Home Page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Render a page that displays the contents of that encyclopedia entry.
def entry(request, title):
    page_content = util.get_entry(title)

    if not page_content:
        return render(request, "encyclopedia/error_page.html", {
            "message": f"{title.capitalize()}, is not part of this Wiki page"
        })

    return render(request, "encyclopedia/entry.html",  {
        "title": title.capitalize(),
        "content": markdown(page_content)
    })


# SEARCH FOR ENTRY
def search(request):
    search_request = request.GET.get("q")
    content = util.get_entry(search_request)
    if not content:
        result = []
        for title in util.list_entries():
            if search_request.casefold() in title.casefold():
                result.append(title)
        return render(request, "encyclopedia/search.html", {
            "result": result,
            "mess": f" {search_request.capitalize()}:  Not listed in this Wiki Page "
        })
    return render(request, "encyclopedia/entry.html", {
        "title": search_request,
        "content": markdown(content)
    })


# CREATE NEW PAGE
def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        for entry in util.list_entries():
            if title.casefold() == entry.casefold():
                return render(request, "encyclopedia/new_page.html", {
                    "message": "Page with same title already exists!",
                    "title": title,
                    "content": content
                })
        util.save_entry(title, content)
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "message": "New encyclopedia page added with success!"
        })
    return render(request, "encyclopedia/new_page.html")



# Edit page
def edit_entry(request, title):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown(content),
            "message": f"{title} has been successfully updated!"
        })
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_entry.html", {
        "title": title,
        "content": content
    })

#random Entry
def random_entry(request):
    title = choice(util.list_entries())
    content = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown(content)
    })

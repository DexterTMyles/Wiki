from django.shortcuts import render
from markdown2 import markdown
from . import util

from django.http import HttpResponse

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

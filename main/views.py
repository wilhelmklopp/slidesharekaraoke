from django.shortcuts import render
from django.http import HttpResponse
import json
import time
import requests
import hashlib
import random
import os
from bs4 import BeautifulSoup

# Create your views here.

api_key = os.environ.get("api_key", "")
shared_secret = os.environ.get("shared_secret", "")


def index(request):
    context = {}
    return render(request, "main/index.html", context)


def completely_random(request):
    timestamp = int(time.time())
    hashed = hashlib.sha1(shared_secret + str(timestamp)).hexdigest()
    url = "https://www.slideshare.net/api/2/get_slideshow"
    random_int = random.randint(11111111, 99999999)
    payload = {"api_key": api_key, "ts": timestamp, "hash": hashed, "detailed": 1, "slideshow_id": random_int}
    r = requests.get(url, data=payload)
    response = r.text
    xml_response = response
    return HttpResponse(xml_response, content_type="application/xhtml+xml")


def tag(request):
    """try:
        minimum_slides = request.GET["min-slides"]
        print minimum_slides
        maximum_slides = request.GET["max-slides"]
        print maximum_slides
        all_languages = request.GET["all-languages"]
        print all_languages
    except Exception as e:
        json_response = {"response": "Insufficient parameters."}
        return HttpResponse(json.dumps(json_response), content_type="application/json")"""

    def get_slideshow_by_random_tag(slidenumbers=20, maxslidenumber=50):
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, "clean_words.json")
        with open(file_path) as data_file:    
            data = json.load(data_file)
        random_int = random.randint(0, len(data))
        random_tag = data[random_int]
        print random_tag

        timestamp = int(time.time())
        hashed = hashlib.sha1(shared_secret + str(timestamp)).hexdigest()

        url = "https://www.slideshare.net/api/2/get_slideshows_by_tag"
        payload = {"api_key": api_key, "ts": timestamp, "hash": hashed, "detailed": 1, "tag": random_tag, "limit": 1}
        r = requests.get(url, data=payload)
        response = r.content
        # print response

        soup = BeautifulSoup(response) 

        print soup

        # error checking

        """error = soup.html.body.attrs
        if error != None:
            json_response = {"success": "false", "error": "SlideShareServiceError", "response": response}
            return json.dumps(json_response)"""
        """try:
            count = soup.html.body.tag.count.contents[0]
        except Exception as e:
            json_response = {"success": "false", "error": "Can't find <tag> node", "code": str(e)}
            return json.dumps(json_response)
        else:
            if count <= 5:
                json_response = {"success": "false", "error": "No slideshows with required tag found"}
                return json.dumps(json_response)"""

        try:
            slide_number = soup.tag.slideshow.numslides.contents[0]
            print slide_number
        except Exception as e:
            json_response = {"success": "false", "error": "Can't find <NumSlides> node", "code": str(e), "response": response}
            return json.dumps(json_response)
        else:
            if int(slide_number) < slidenumbers:
                json_response = {"success": "false", "error": "Number of Slides lower than required"}
                return json.dumps(json_response)
            elif int(slide_number) > maxslidenumber:
                json_response = {"success": "false", "error": "Number of Slides greater than required"}
                return json.dumps(json_response)

        try:
            slide_url = soup.tag.slideshow.url.contents[0]
        except Exception as e:
            json_response = {"success": "false", "error": "Can't find <url> node", "code": str(e)}
            return json.dumps(json_response)
        else:
            json_response = {"success": "true", "slide_url": slide_url, "response": response}
            return json.dumps(json_response)

        """try:
            language = soup.html.body.tag.slideshow.language.contents[0]
            print language
        except Exception as e:
            json_response = {"success": "false", "error": "Can't find <language> node", "code": str(e)}
            return json.dumps(json_response)
        else:
            if str(all_languages).lower() == "false" and str(language) != "en":
                json_response = {"success": "false", "error": "Not the right language", "code": str(e)}
                return json.dumps(json_response)"""


    no_success = True
    while(no_success):
        result = json.loads(get_slideshow_by_random_tag())
        if result["success"]=="true":
            slide_url = result["slide_url"]
            response = result["response"]
            no_success = False
        """else:
            print result["error"]
            print result["code"]
            print result["response"]"""

    json_response = {"slide_url": slide_url}

    return HttpResponse(json.dumps(json_response), content_type="application/json")


def test(request):
    context = {}
    return render(request, "main/test.html", context)
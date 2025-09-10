from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from groq import Groq
from PIL import Image
from rembg import remove
from requests import post
from io import BytesIO
import json
import os

# ✅ Home page

def Home(request):
    context = {
        'user': request.user
    }
    return render(request, "screens/index.html", context=context)

# ✅ About Us page
def about_us(request):
    context = {
        'user': request.user
    }
    return render(request, "screens/about_us.html", context=context)

# ✅ AI Chat
GROQ_API_KEY = getattr(settings, "GROQ_API_KEY", "your_default_key_here")

@login_required
@csrf_exempt
def AIChat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            prompt = data.get("prompt", "").strip()

            if not prompt:
                return JsonResponse({"error": "No prompt provided."}, status=400)

            client = Groq(api_key=GROQ_API_KEY)

            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                model="llama3-8b-8192",
            )

            response_text = chat_completion.choices[0].message.content.strip()
            return JsonResponse({"prompt": prompt, "result": response_text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "screens/ai_chat.html", context={"prompt": "", "result": "", "user": request.user})

# ✅ Background Remover
@login_required
def bgRemover(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        name = request.POST.get("name")
        print("Please wait, this may take a few seconds...")

        save_directory = os.path.join('static', 'images', 'bgremover', 'before')
        os.makedirs(save_directory, exist_ok=True)
        fs = FileSystemStorage(location=save_directory)
        saved_file_path = fs.save(file.name, file)
        img_path = fs.url(saved_file_path)
        full_image_path = os.path.join(save_directory, saved_file_path)

        print("Saved file path:", full_image_path)

        x = Image.open(full_image_path)
        res = remove(x)

        final_image_name = name + ".png"
        final_save_path = os.path.join('static', 'images', 'bgremover', 'after', final_image_name)
        res.save(final_save_path)

        print("Finished! Have a look at it.")

        context = {
            "isRemoved": True,
            "before": file.name,
            "after": final_image_name,
            "user": request.user
        }
        return render(request, "screens/bg_remover.html", context=context)

    return render(request, "screens/bg_remover.html", context={"user": request.user})

# ✅ AI Image Generation
@login_required
def imgGeneration(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        response = post(
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
            headers={"Authorization": "Bearer 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"},
            json={"inputs": prompt},
            stream=True
        )
        image = Image.open(BytesIO(response.content))
        img_name = f"{prompt}(Ai_generated).png"
        save_path = os.path.join("static", "images", "ai", img_name)
        image.save(save_path)

        context = {
            "image": True,
            "name": img_name,
            "user": request.user
        }
    else:
        context = {
            "image": False,
            "user": request.user
        }

    return render(request, "screens/ai_image_generator.html", context=context)

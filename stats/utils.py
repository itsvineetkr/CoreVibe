import os
from stats.models import *
from django.utils import timezone
from huggingface_hub import InferenceClient

from dotenv import load_dotenv
import os

load_dotenv()

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")


def get_user_display_data(user):
    data = {}

    physicalData = UserPhysicalData.objects.get(user=user)
    data["physicalData"] = physicalData

    try:
        dailyStats = UserDailyStats.objects.get(user=user, date=timezone.now())
        data["dailyStats"] = dailyStats
    except:
        dailyStats = UserDailyStats(user=user, sleep="00:00")
        dailyStats.save()
        data["dailyStats"] = dailyStats

    goals = UserGoals.objects.get(user=user)
    data["goals"] = goals

    percentStats = {
        "steps": (dailyStats.steps / goals.steps) * 100,
        "water": (dailyStats.water / goals.water) * 100,
        "active": (dailyStats.active / goals.active) * 100,
        "kcal": (dailyStats.kcal / goals.kcal) * 100,
    }

    data["percentStats"] = percentStats

    bmi = round(physicalData.weight / ((physicalData.height / 100) ** 2), 2)
    percentage_bmi = (bmi / 30) * 100
    percentage_bmi = 30 if percentage_bmi > 30 else percentage_bmi

    data["bmi"] = {"percentage": percentage_bmi, "bmi": bmi}

    data["textResponse"] = {"am_i_healthy": "", "how_was_my_day": ""}

    """
    {
        physicalData = {
            user, height, weight, age, gender, date_updated
        }

        dailyStats = {
            user, steps, water, active, kcal, sleep, date
        }

        goals = {
            user, steps, water, active, kcal, sleep, date
        }

        percentStats = {
            steps, water, active, kcal
        }

        bmi = {
            percentage, bmi
        }

        textResponse = {
            am_i_healthy, how_was_my_day
        }
    }
    """

    return data


def generate_response(prompt):
    client = InferenceClient(api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"))
    initPrompt = """
    You are an AI assistant that can answer questions about health and wellness. 
    You are given data of user related to their physical health.
    You need to give answer to the question asked after the data.
    The answer must be in paragraph and not too long.
    """
    response = client.chat_completion(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=[
                {
                    "role": "system",
                    "content": initPrompt
                },
                {
                    "role": "user",
                    "content": prompt,
                },
        ],
        max_tokens=500,
        stream=False,
    )

    return response["choices"][0]["message"]["content"]

def generate_prompt(action, data):
    if action == "am_i_healthy":
        return f"Data: age is {data['physicalData'].age}, gender is {data['physicalData'].gender}, weight is {data['physicalData'].weight} and height is {data['physicalData'].height} and today I walked {data['dailyStats'].steps} steps and burned {data['dailyStats'].kcal} calories, Am I healthy?"
    if action == "how_was_my_day":
        return f"Data: age is {data['physicalData'].age}, gender is {data['physicalData'].gender}, weight is {data['physicalData'].weight} and height is {data['physicalData'].height} and today I walked {data['dailyStats'].steps} steps, burned {data['dailyStats'].kcal} calories, drank {data['dailyStats'].water} ml Water and was active for {data['dailyStats'].active} mins, how was my day so far according to this data?."

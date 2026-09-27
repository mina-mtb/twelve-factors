# Example: Using requirements.txt
FROM python:3.13-alpine

WORKDIR /app

"""
#  اول یک ارگومان تعریف میکنیم برای این کار که در زمان بیلد داکر این ارگومان مقدار دهی میشود و چون این متغیر فقط برا همین محیط است بعد از زمان بیلد از بین میرود اما ما ان را برای زمان اجرای کانتینر هم نیاز داریم پس مقادارش را در یک متغیر در ای ان وی میریزیم که بعد در زمان اجرای کانتینر بتوانیم از ان استفاده کنیم 
ARG IMAGE_SOURCE=unknown
ARG APP_VERSION=unknown

# دی اینجا فقط مقدار دا در متغیری در ای ان وی ریختیم که برای زمان اجرای کانتینر قابل دسسترسی باشد
ENV IMAGE_SOURCE=$IMAGE_SOURCE
ENV APP_VERSION=$APP_VERSION

"""

# Copy only the requirements file first
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Now copy the rest of the application code
COPY main.py .
COPY .env .

# Define how to run the application (example)
CMD ["python", "main.py"]

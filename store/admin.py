import csv
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django import forms
from .models import Product

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]

            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Not a CSV file")
                return redirect("..")

            file_data = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(file_data)

            count_new = 0
            count_updated = 0

            for row in reader:
                obj, created = Product.objects.update_or_create(
                    name=row['name'],   # unique field
                    defaults={
                        'category': row['category'],
                        'brand': row['brand'],
                        'price': float(row['price']),
                        'description': row['description']
                    }
                )

                if created:
                    count_new += 1
                else:
                    count_updated += 1

            messages.success(
                request,
                f"CSV Uploaded! New: {count_new}, Updated: {count_updated}"
            )

            return redirect("..")

        form = CsvImportForm()
        return render(request, "admin/csv_upload.html", {"form": form})


from .models import Product, UserInteraction

admin.site.register(Product, ProductAdmin)
admin.site.register(UserInteraction)
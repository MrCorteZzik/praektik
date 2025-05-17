from django import forms
from .models import Product, ProductImage
import mimetypes

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock']

class ProductImageForm(forms.Form):
    images = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': True, 'accept': 'image/*'}),
        label='Изображения',
        required=True
    )

    def clean_images(self):
        images = self.files.getlist('images')
        if not images:
            raise forms.ValidationError('Пожалуйста, загрузите хотя бы одно изображение.')
        for image in images:
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('Изображение слишком большое! Максимум 5MB.')
            mime_type, _ = mimetypes.guess_type(image.name)
            if mime_type not in ['image/png', 'image/jpeg', 'image/gif']:
                raise forms.ValidationError('Поддерживаются только PNG, JPEG и GIF!')
        return images
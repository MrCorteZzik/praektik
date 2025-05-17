from django import forms
from .models import Product, ProductImage
import mimetypes

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock']

class ProductImageForm(forms.Form):
    image1 = forms.FileField(
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        label='Изображение 1',
        required=True
    )
    image2 = forms.FileField(
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        label='Изображение 2',
        required=False
    )
    image3 = forms.FileField(
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        label='Изображение 3',
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        images = [cleaned_data.get('image1'), cleaned_data.get('image2'), cleaned_data.get('image3')]
        images = [img for img in images if img]  # Remove None values
        if not images:
            raise forms.ValidationError('Пожалуйста, загрузите хотя бы одно изображение.')
        for image in images:
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('Изображение слишком большое! Максимум 5MB.')
            mime_type, _ = mimetypes.guess_type(image.name)
            if not mime_type or mime_type not in ['image/png', 'image/jpeg', 'image/gif']:
                raise forms.ValidationError('Поддерживаются только PNG, JPEG и GIF!')
        cleaned_data['images'] = images
        return cleaned_data
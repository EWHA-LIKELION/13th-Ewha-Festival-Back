import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from booths.models import Booth, OperatingHours, Menu
from image_def import ImageProcessing  # S3 업로드를 위한 유틸

def create_booth(request):
    if request.method == "POST":
        name = request.POST.get('name')
        category = request.POST.get('category')
        contact = request.POST.get('contact')
        location = request.POST.get('location')
        booth_num = request.POST.get('booth_num')
        description = request.POST.get('description')
        is_show = True if request.POST.get('is_show') == 'on' else False

        try:
            booth_num = int(booth_num)
        except (TypeError, ValueError):
            messages.error(request, "부스 번호는 숫자여야 합니다.")
            return redirect('collects:create_booth')

        # 썸네일 S3 업로드
        thumbnail_file = request.FILES.get('thumbnail')
        thumbnail_url = ''
        if thumbnail_file:
            filename = f'{location[:-1]}{int(booth_num):02}' if location.endswith('관') else f'{location}{int(booth_num):02}'
            thumbnail_url = ImageProcessing.s3_file_upload_by_file_data(thumbnail_file, "booth_thumbnail", f"{filename}.jpg")

        booth = Booth.objects.create(
            name=name,
            category=category,
            contact=contact,
            location=location,
            description=description,
            is_opened=True,
            is_show=is_show,
            booth_num=booth_num,
            code="BOOTH-" + uuid.uuid4().hex[:8],
            thumbnail=thumbnail_url
        )

        operating_hours_data = [
            {"date": 14, "day_of_week": "수요일", "open_time": request.POST.get("open_time_14"), "close_time": request.POST.get("close_time_14")},
            {"date": 15, "day_of_week": "목요일", "open_time": request.POST.get("open_time_15"), "close_time": request.POST.get("close_time_15")},
            {"date": 16, "day_of_week": "금요일", "open_time": request.POST.get("open_time_16"), "close_time": request.POST.get("close_time_16")},
        ]
        operating_hours_instances = [OperatingHours(booth=booth, **data) for data in operating_hours_data]
        OperatingHours.objects.bulk_create(operating_hours_instances)

        messages.success(request, "부스가 성공적으로 등록되었습니다.")
        return redirect('collects:booth_list')

    return render(request, 'create_booth.html')

def create_menu(request):
    if request.method == "POST":
        booth_ids = request.POST.getlist('booth')
        names = request.POST.getlist('name')
        prices = request.POST.getlist('price')
        thumbnails = request.FILES.getlist('thumbnail')

        if not (len(booth_ids) == len(names) == len(prices)):
            messages.error(request, "입력한 데이터에 오류가 있습니다.")
            return redirect('collects:create_menu')

        if len(thumbnails) < len(booth_ids):
            thumbnails.extend([None] * (len(booth_ids) - len(thumbnails)))

        for i in range(len(names)):
            try:
                booth = Booth.objects.get(id=booth_ids[i])
            except Booth.DoesNotExist:
                messages.error(request, "유효하지 않은 부스가 선택되었습니다.")
                continue
            try:
                price = float(prices[i])
            except ValueError:
                messages.error(request, "가격 형식이 올바르지 않습니다.")
                continue

            thumbnail_file = thumbnails[i]
            thumbnail_url = ''
            if thumbnail_file:
                filename = f'{booth.location}_{booth.booth_num}_{names[i]}'
                thumbnail_url = ImageProcessing.s3_file_upload_by_file_data(thumbnail_file, "menu_thumbnail", f"{filename}.jpg")

            Menu.objects.create(
                booth=booth,
                name=names[i],
                price=price,
                thumbnail=thumbnail_url
            )

        messages.success(request, "메뉴가 성공적으로 등록되었습니다.")
        booth_id = booth_ids[0]
        return redirect('collects:detail', booth_id=booth_id)

    booths = Booth.objects.all()
    selected_booth = None
    booth_id = request.GET.get('booth_id')
    if booth_id:
        try:
            selected_booth = Booth.objects.get(id=booth_id)
        except Booth.DoesNotExist:
            selected_booth = None

    return render(request, 'create_menu.html', {'booths': booths, 'selected_booth': selected_booth})

def booth_list(request):
    booths = Booth.objects.all().order_by('-created_at')
    return render(request, 'booth_list.html', {'booths': booths})

def edit_booth(request, booth_id):
    booth = get_object_or_404(Booth, id=booth_id)

    if request.method == "POST":
        booth.name = request.POST.get('name')
        booth.location = request.POST.get('location')
        booth.booth_num = request.POST.get('booth_num')
        booth.category = request.POST.get('category')
        booth.contact = request.POST.get('contact')
        booth.description = request.POST.get('description', '')

        thumbnail = request.FILES.get('thumbnail')
        if thumbnail:
            filename = f'{booth.location[:-1]}{int(booth.booth_num):02}' if booth.location.endswith('관') else f'{booth.location}{int(booth.booth_num):02}'
            thumbnail_url = ImageProcessing.s3_file_upload_by_file_data(thumbnail, "booth_thumbnail", f"{filename}.jpg")
            booth.thumbnail = thumbnail_url

        try:
            booth.booth_num = int(booth.booth_num)
        except (TypeError, ValueError):
            messages.error(request, "부스 번호는 숫자여야 합니다.")
            return redirect('collects:edit_booth', booth_id=booth.id)

        booth.save()
        messages.success(request, "부스가 성공적으로 수정되었습니다.")
        return redirect('collects:booth_list')

    return render(request, 'edit_booth.html', {'booth': booth})

def edit_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)

    if request.method == "POST":
        menu.name = request.POST.get('name')
        try:
            menu.price = float(request.POST.get('price'))
        except ValueError:
            messages.error(request, "가격 형식이 올바르지 않습니다.")
            return redirect('collects:edit_menu', menu_id=menu.id)

        thumbnail = request.FILES.get('thumbnail')
        if thumbnail:
            filename = f'{menu.booth.location}_{menu.booth.booth_num}_{menu.name}'
            thumbnail_url = ImageProcessing.s3_file_upload_by_file_data(thumbnail, "menu_thumbnail", f"{filename}.jpg")
            menu.thumbnail = thumbnail_url

        menu.save()
        messages.success(request, "메뉴가 성공적으로 수정되었습니다.")
        return redirect('collects:detail', booth_id=menu.booth.id)

    return render(request, 'edit_menu.html', {'menu': menu})

def home(request):
    return render(request, 'home.html')

def detail(request, booth_id):
    booth = get_object_or_404(Booth, id=booth_id)
    return render(request, 'detail.html', {'booth': booth})

import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from booths.models import Booth, OperatingHours, Menu

def create_booth(request):
    if request.method == "POST":
        # 부스 정보 받기
        name = request.POST.get('name')
        category = request.POST.get('category')
        contact = request.POST.get('contact')
        location = request.POST.get('location')
        booth_num = request.POST.get('booth_num')
        description = request.POST.get('description')
        thumbnail = request.FILES.get('thumbnail')
        is_show = True if request.POST.get('is_show') == 'on' else False


        try:
            booth_num = int(booth_num)
        except (TypeError, ValueError):
            messages.error(request, "부스 번호는 숫자여야 합니다.")
            return redirect('collects:create_booth')

        # 부스 객체 생성
        booth = Booth.objects.create(
            name=name,
            category=category,
            contact=contact,
            location=location,
            description=description,
            is_opened=True,  # 기본값으로 활성화
            is_show=is_show,  
            booth_num=booth_num,    
            code = "BOOTH-" + uuid.uuid4().hex[:8], 
            thumbnail=thumbnail if thumbnail is not None else ''
        )

        # 날짜별 운영 시간 데이터 받기
        operating_hours_data = [
            {"date": 14, "day_of_week": "수요일", "open_time": request.POST.get("open_time_14"), "close_time": request.POST.get("close_time_14")},
            {"date": 15, "day_of_week": "목요일", "open_time": request.POST.get("open_time_15"), "close_time": request.POST.get("close_time_15")},
            {"date": 16, "day_of_week": "금요일", "open_time": request.POST.get("open_time_16"), "close_time": request.POST.get("close_time_16")},
        ]

        # OperatingHours 모델에 데이터 저장
        operating_hours_instances = [
            OperatingHours(booth=booth, **data) for data in operating_hours_data
        ]
        OperatingHours.objects.bulk_create(operating_hours_instances)  # 한 번에 저장

        messages.success(request, "부스가 성공적으로 등록되었습니다.")
        return redirect('collects:booth_list')  

    return render(request, 'create_booth.html')



def create_menu(request):
    if request.method == "POST":
        # 여러 메뉴 항목의 값을 리스트로 받음
        booth_ids = request.POST.getlist('booth')
        names = request.POST.getlist('name')
        prices = request.POST.getlist('price')
        thumbnails = request.FILES.getlist('thumbnail')

        # 데이터 개수 일치 처리
        if not (len(booth_ids) == len(names) == len(prices)):
            messages.error(request, "입력한 데이터에 오류가 있습니다.")
            return redirect('collects:create_menu')
        
        if len(thumbnails) < len(booth_ids):
            thumbnails.extend([None] * (len(booth_ids) - len(thumbnails)))
        
        # 각 항목별로 Menu 객체 생성
        for i in range(len(names)):
            try:
                booth = Booth.objects.get(id=booth_ids[i])
            except Booth.DoesNotExist:
                messages.error(request, "유효하지 않은 부스가 선택되었습니다.")
                continue  # 해당 항목은 건너뜁니다.
            try:
                price = float(prices[i])
            except ValueError:
                messages.error(request, "가격 형식이 올바르지 않습니다.")
                continue

            Menu.objects.create(
                booth=booth,
                name=names[i],
                price=price,
                thumbnail=thumbnails[i] or ''
            )
        messages.success(request, "메뉴가 성공적으로 등록되었습니다.")
        booth_id = booth_ids[0]
        return redirect('collects:detail', booth_id=booth_id)
    
    # GET 요청 시 부스 목록을 전달하여 드롭다운 옵션으로 사용
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
    return render(request, 'booth_list.html', {'booths':booths})


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
            booth.thumbnail = thumbnail
        
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
            menu.thumbnail = thumbnail
        
        menu.save()
        messages.success(request, "메뉴가 성공적으로 수정되었습니다.")
        return redirect('collects:detail', booth_id=menu.booth.id)
    
    return render(request, 'edit_menu.html', {'menu': menu})

def home(request):
    return render(request, 'home.html')

def detail(request, booth_id):
    booth = get_object_or_404(Booth, id=booth_id)
    return render(request, 'detail.html', {'booth': booth})
import os 
from django.shortcuts import render, HttpResponse, redirect 
from .models import * 
from .forms import * 
import face_recognition 
import cv2 
import numpy as np 
from .send_email import send_email 
from datetime import datetime 
 
last_face = 'no_face' 
 
def index(request): 
    scanned = LastFace.objects.all().order_by('date').reverse() 
    present = Profile.objects.filter(st='pr').order_by('updated').reverse() 
    absent = Profile.objects.filter(st='abs').order_by('shift') 
    late = Profile.objects.filter(st='late').order_by('updated').reverse() 
    last_face = LastFace.objects.last() 
    profile = Profile.objects.get(image__icontains=last_face) 
 
    context = { 
        'scanned': scanned, 
        'present': present, 
        'absent': absent, 
        'late': late, 
        'profile': profile 
    } 
    return render(request, 'core/index.html', context) 
 
def mainpage(request): 
    LastFace.objects.all().delete() 
    return render(request, 'core/mainpage.html') 
 
 
def ajax(request): 
    last_face = LastFace.objects.last() 
    context = { 
        'last_face': last_face 
    } 
    return render(request, 'core/ajax.html', context) 
 
def scan(request): 
    global last_face 
 
    known_face_encodings = [] 
    known_face_names = [] 
 
    profiles = Profile.objects.all() 
    for profile in profiles: 
        person = profile.image 
        image_of_person = face_recognition.load_image_file(f'media/{person}') 
        person_face_encoding = np.loadtxt(f'{profile.first_name}.txt') 
        person_face_encoding = face_recognition.face_encodings(image_of_person)[0] 
        np.savetxt(f"{profile.first_name}.txt", person_face_encoding ) 
        known_face_encodings.append(person_face_encoding) 
        known_face_names.append(f'{person}'[:-4]) 
        print('Известные лица:', known_face_names) 
 
    # RTSP_URL = 'rtsp://admin:admin12345@192.168.28.220:554/cam/realmonitor?channel=1&subtype=1' 
 
    # os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp' 
 
    # video_capture = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG) 
    video_capture = cv2.VideoCapture(0) 
 
    face_locations = [] 
    face_encodings = [] 
    face_names = [] 
    process_this_frame = True 
    while True: 
        ret, frame = video_capture.read() 


        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) 
        rgb_small_frame = small_frame[:, :, ::-1] 

 
        if process_this_frame: 
            face_locations = face_recognition.face_locations(frame) 
            face_encodings = face_recognition.face_encodings( 
                frame, face_locations) 
 
            face_names = [] 
            for face_encoding in face_encodings: 
                matches = face_recognition.compare_faces( 
                    known_face_encodings, face_encoding) 
                name = "Unknown" 
 
                face_distances = face_recognition.face_distance( 
                    known_face_encodings, face_encoding) 
                best_match_index = np.argmin(face_distances) 
                if matches[best_match_index]: 
                    name = known_face_names[best_match_index] 
                    print('Лучшее совпадение:', name) 
                    profile = Profile.objects.get(image__icontains=name) 
                    print('Профиль этого лица:', profile) 
                    late_mes = '' 
                    if profile.st == 'pr' or profile.st == 'late': 
                        print('Вы уже отмечены как',profile.st) 
                    else: 
                        print('Сейчас мы вас отметим.') 
                        if datetime.now().time() > profile.shift: 
                            profile.st = 'late' 
                            late_mes = ' and late' 
                        else: 
                            profile.st = 'pr' 
                            late_mes = ' and came on time' 
                        profile.save() 
                        #почта 
                        send_to = str(profile.email) 
                        # must_came = str(profile.shift.strftime("%H %M %S")) 
                        # tim = str(profile.updated.strftime("%H %M %S")) 
                        # content = profile.first_name + ' ' + profile.last_name + ' was marked at time ' + tim + late_mes + 'he must came in' + must_came 
                        # send_email(send_to, content) 
                    last_face = LastFace(last_face=name) 
                    last_face.save() 
                    last_face = name 
                face_names.append(name) 
 
        process_this_frame = not process_this_frame 
 
        for (top, right, bottom, left), name in zip(face_locations, face_names): 
            # top *= 4 
            # right *= 4 
            # bottom *= 4 
            # left *= 4 
 
            frame = cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2) 
 
            frame = cv2.rectangle(frame, (left, bottom - 35), 
                          (right, bottom), (0, 0, 255), cv2.FILLED) 
            font = cv2.FONT_HERSHEY_DUPLEX 
            frame = cv2.putText(frame, name, (left + 6, bottom - 6), 
                        font, 0.5, (255, 255, 255), 1) 
 
        cv2.imshow('Video', frame) 
 
        if cv2.waitKey(1) & 0xFF == 13: 
            break 
 
    video_capture.release() 
    cv2.destroyAllWindows() 
    return HttpResponse('scaner closed', last_face) 
 
def login(request): 
    try: 
        last_face = LastFace.objects.last() 
        profile = Profile.objects.get(image__icontains=last_face)   
        return redirect('index') 
    except: 
        last_face = None 
        profile = None 
        context = { 
            'profile': profile, 
            'last_face': last_face 
        } 
        return render(request, 'core/login.html', context) 
 
 
def register(request): 
    form = ProfileForm 
    if request.method == 'POST': 
        form = ProfileForm(request.POST,request.FILES) 
        if form.is_valid(): 
            print('Форма правильно заполнена') 
            form.save() 
            return redirect('mainpage') 
        else: 
            print('Форма неправильно заполнена:') 
            print(form.errors) 
    context ={'form':form} 
    return render(request,'core/register.html',context)
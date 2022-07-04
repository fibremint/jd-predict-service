from decouple import config

def main():
    # sample_jd = {
    #     'position': '머신러닝 엔지니어',
    #     'main_tasks': "딥러닝 백엔드 서비스 개발 및 유지보수\n",
    #     'requirements': "백엔드 프레임워크 (Django, Node.js 등등)를 기반으로 한 백엔드 서비스 개발 경험\n머신러닝에 대한 이해\n데이터베이스 구축 경험",
    #     'preferred_points': "딥러닝 프로젝트 경험"
    # }

    # desired prediction: 개발 
    sample_jd = {
        "wd_id": 42,
        "position": "머신러닝 엔지니어",
        "main_tasks": "딥러닝 백엔드 서비스 개발 및 유지보수\n",
        "requirements": "백엔드 프레임워크 (Django, Node.js 등등)를 기반으로 한 백엔드 서비스 개발 경험\n머신러닝에 대한 이해\n데이터베이스 구축 경험",
        "preferred_points": "딥러닝 프로젝트 경험"
    }

    # desired prediction: 디자인
    sample_jd = {
        "wd_id": 42,
        "position": "UI/UX 담당",
        "main_tasks": "사용자 인터페이스 구성\n",
        "requirements": "포토샵 사용 경험",
        "preferred_points": ""
    }

    headres = {
        "accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
    }

    import json
    sample_jd = json.dumps(sample_jd)

    import requests
    request_base_address = config('EXPOSE_PROTOCOL') + '://' + config('API_EXPOSE_HOST_ADDR') + ':' + config('API_EXPOSE_PORT')
    res = requests.post(request_base_address + '/predict', data=sample_jd, headers=headres)
    print(res.text)


if __name__ == '__main__':
    main()

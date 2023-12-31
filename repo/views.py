from django.shortcuts import render
import requests
from datetime import datetime


def is_valid_github_username(username):
    api_url = f'https://api.github.com/users/{username}'
    response = requests.get(api_url)
    return response.status_code == 200


def fetch_all_user_repositories(username):
    repositories = []
    page = 1
    per_page = 50  # Number of repositories per page
    while True:
        api_url = f'https://api.github.com/users/{username}/repos?page={page}&per_page={per_page}'
        response = requests.get(api_url)
        if response.status_code != 200:
            break
        page_repositories = response.json()
        if not page_repositories:
            break
        repositories.extend(page_repositories)
        page += 1
    return repositories


def search_form(request):
    return render(request, 'repo/index.html')


def search_results(request):
    if request.method == 'POST':
        username = request.POST['username']
        language = request.POST['language']

        if not is_valid_github_username(username):
            error_message = 'Invalid GitHub username. Please check your username.'
            return render(request, 'repo/index.html', {'error_message': error_message})

        # Fetch all repositories
        repositories = fetch_all_user_repositories(username)

        # Filter repositories by the specified language
        if language:
            language = language.lower()
            filtered_repositories = [
                repo for repo in repositories if repo['language'] and repo['language'].lower() == language]
        else:
            filtered_repositories = repositories

        for repo in filtered_repositories:
            if repo['pushed_at']:
                pushed_at = datetime.fromisoformat(repo['pushed_at'][:-1])
                repo['formatted_pushed_at'] = pushed_at.strftime('%B %d, %Y')

        context = {
            'repositories': filtered_repositories,
            'language': language,
            'username': username,
        }
        return render(request, 'repo/repos.html', context)
    else:
        return search_form(request)

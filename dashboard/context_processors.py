from django.urls import include


def check_active_sidebar_links(request):
    current_url = request.resolver_match.url_name
    active_url = "index"
    jobs_url_status = False
    verify_org_url_status = False
    register_staff_url_status = False

    # checking job urls active status
    job_urls = ["jobs_list", "jobs_create", "jobs_update"]
    job_category_urls = ["category_list", "category_create", "category_update"]
    job_combine_urls = job_urls + job_category_urls

    if current_url in job_combine_urls:
        jobs_url_status = True

    # checking verify organization urls active status
    verify_org_urls = ["verify_organization_list", "verify_organization"]
    if current_url in verify_org_urls:
        verify_org_url_status = True

    # checking verify organization urls active status
    register_staff_urls = ["staff_register_list",
                           "staff_register_create", "staff_register_update"]
    if current_url in register_staff_urls:
        register_staff_url_status = True

    if current_url in job_category_urls:
        active_url = "job-category"
    elif current_url in job_urls:
        active_url = "jobs"
    elif current_url in verify_org_urls:
        active_url = "verify-organization"
    elif current_url in register_staff_urls:
        active_url = "register-staff"

    context = {
        'current_url': current_url,
        'active_url': active_url,
        'jobs_url_status': jobs_url_status,
        'verify_org_url_status': verify_org_url_status,
        'register_staff_url_status': register_staff_url_status,
    }
    return context

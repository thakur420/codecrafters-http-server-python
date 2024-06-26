def extract_path(request):
    request_lines = request.splitlines()
    if request_lines:
        request_line = request_lines[0]
        parts = request_line.split()
        if len(parts) > 1:
            return parts[1]
        return ""
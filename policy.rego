package httpapi.authz

default allow = true

deny {
    input.request.method == "POST"
    input.request.path == "/v1/chat/completions"
    input.request.body.prompt
    contains(input.request.body.prompt, "malicious")
}

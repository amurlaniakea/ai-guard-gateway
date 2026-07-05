package httpapi.authz

default allow = false

allow { 
    input.role == 'premium'
}

allow { 
    not contains(input.prompt, "malicious")
}
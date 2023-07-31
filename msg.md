{% for message in messages %}
<div class="mt-4 alert alert-primary alert.dismissible fade show text-center {{ message.tags }}" 
role="alert">
    {{ message }}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
{% endfor %}
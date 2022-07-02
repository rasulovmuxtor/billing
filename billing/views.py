import stripe
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from student.models import Student, Transaction, TransactionType
from django.shortcuts import get_object_or_404, redirect, render
from decimal import Decimal


class IndexView(TemplateView):
    template_name = 'index.html'


def student_detail(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        date_of_birth = request.POST.get('date_of_birth')
        try:
            student = Student.objects.get(id=student_id, date_of_birth=date_of_birth)
        except Student.DoesNotExist:
            return HttpResponse("Student does not exists!")
        return render(request, 'student.html', {'student': student})
    return redirect('index')


@csrf_exempt
def student_checkout_session(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        amount = Decimal(request.POST.get('amount'))
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=student.id,
                success_url=domain_url,
                cancel_url=domain_url,
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': f"TARIFF: {student.get_tariff().title}",
                        'quantity': 1,
                        'currency': 'uzs',
                        'amount': int(amount * 100),
                    }
                ]
            )
            url = checkout_session['url']
            return redirect(url)
        except Exception as e:
            return JsonResponse({'error': str(e)})


def handle_checkout_session(session):
    client_reference_id = session.get("client_reference_id")
    payment_intent = session.get("payment_intent")
    amount_total = Decimal(session.get('amount_total'))
    if client_reference_id is None:
        # Customer wasn't logged in when purchasing
        return
    Transaction.objects.create(
        student_id=client_reference_id,
        amount=amount_total / 100,
        identifier=payment_intent,
        type=TransactionType.stripe
    )


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)

    return HttpResponse(status=200)

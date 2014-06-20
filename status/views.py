from django.shortcuts import render_to_response
from django.template import RequestContext

from sniffer.proc_utils import monitor

from status.models import Status

def index(request):
    monitor()
    return render_to_response(
        "hyframework/index.htm",
        {'status_list' : Status.objects.all()},
        RequestContext(request, {}),
    )
    
def change_status(request, proc, new_status):
    
    print proc
    print new_status
    
    if proc == 'Sniffer':
        from sniffer import hysniff
        if new_status == 'True':
            hysniff.do_sniff()
    elif proc == 'SSLStrip':
        if new_status == 'True':
            from sniffer.proc_utils import run_helpers
            run_helpers('sslstrip')
        elif new_status == 'False':
            from sniffer.proc_utils import kill_helpers 
            kill_helpers('ssltrip')
    elif proc == 'ARPSpoof':
        if new_status == 'True':
            from sniffer.proc_utils import run_helpers 
            run_helpers('arpspoof')
        elif new_status == 'False':
            from sniffer.proc_utils import kill_helpers 
            kill_helpers('arpspoof')
    return render_to_response(
        "hyframework/index.htm",
        {'status_list' : Status.objects.all()},
        RequestContext(request, {}),
        )
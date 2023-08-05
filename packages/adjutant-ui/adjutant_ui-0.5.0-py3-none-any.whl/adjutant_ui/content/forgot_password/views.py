# Copyright (c) 2016 Catalyst IT Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.shortcuts import render

from horizon import forms

from adjutant_ui.content.forgot_password import forms as fp_forms


class ForgotPasswordView(forms.ModalFormView):
    form_class = fp_forms.ForgotPasswordForm
    template_name = 'forgot_password/index.html'
    success_url = '/forgot_password/sent'


def password_sent_view(request):
    return render(request, 'forgot_password/sent.html')

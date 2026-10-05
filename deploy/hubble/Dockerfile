FROM hugegraph/hubble:1.7.0
COPY default-language.js /hubble/ui/static/js/eoip-default-language.js
RUN test "$(grep -o '<head>' /hubble/ui/index.html | wc -l)" -eq 1 && \
    sed -i 's@<head>@<head><script src="/static/js/eoip-default-language.js"></script>@' /hubble/ui/index.html

FROM hugegraph/hubble:1.7.0
COPY deploy/hubble/default-language.js /hubble/ui/static/js/eoip-default-language.js
COPY deploy/hubble/enterprise.html deploy/hubble/enterprise.css deploy/hubble/enterprise.js /hubble/ui/
COPY demo/demodata/enterprise/scenario-pack.json /hubble/ui/enterprise-scenarios.json
RUN test "$(grep -o '<head>' /hubble/ui/index.html | wc -l)" -eq 1 && \
    sed -i 's@<head>@<head><script src="/static/js/eoip-default-language.js"></script>@' /hubble/ui/index.html

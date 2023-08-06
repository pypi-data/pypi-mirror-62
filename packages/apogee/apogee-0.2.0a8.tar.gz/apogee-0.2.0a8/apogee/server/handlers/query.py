import json
from tornado.web import RequestHandler


class QueryHandler(RequestHandler):
    def initialize(self, model, **kwargs) -> None:
        self._model = model
        super().initialize(**kwargs)

    @staticmethod
    def _format_response(dist):
        dist = {k: {s: float(p) for s, p in v.items()} for k, v in dist.items()}
        return json.dumps(dist)

    def post(self, *args, **kwargs) -> None:
        """
        Execute a query against the provided model.

        {
            "marginals": ["asia"],
            "evidence": {"SMOKER": yes}
        }
        """

        data = self.request.body.decode("utf-8")
        if len(data) > 0:
            payload = json.loads(data)
            evidence = payload.get("evidence")
            marginals = payload.get("marginals", {})
            dist = self._model.predict(evidence)
            dist = {k: v for k, v in dist.items() if k in marginals}
        else:
            dist = self._model.predict()

        self.write(self._format_response(dist))

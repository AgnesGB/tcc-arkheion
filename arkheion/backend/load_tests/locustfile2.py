from locust import HttpUser, task, between


class UsuarioArkheion(HttpUser):
    # Simula um usuário que espera entre 1 e 3 segundos entre cada ação (para não parecer um ataque DDoS irreal)
    wait_time = between(1, 3)

    @task(2)
    def acessar_admin(self):
        # Simula o usuário tentando acessar a área administrativa. Isso força o Django a carregar templates e verificar sessão.
        self.client.get("/admin/login/")

    @task(1)
    def acessar_raiz_api(self):
        # Simula o usuário acessando a raiz da API ou a home.
        self.client.get("/")

    def on_start(self):
        # Este método roda quando o "usuário virtual" nasce. Pode ser usado para fazer login, se necessário.
        pass

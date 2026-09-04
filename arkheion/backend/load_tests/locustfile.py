# Este código simula um usuário entrando no sistema e carregando a lista de perícias.

from locust import HttpUser, task, between


class UsuarioCurioso(HttpUser):
    # Simula um tempo de espera entre tarefas (ex: usuário lendo a tela) entre 1 e 5 segundos
    wait_time = between(1, 5)

    @task
    def listar_pericias(self):
        self.client.get("/api/pericias/")

    # @task
    # def pagina_admin(self):
    #     self.client.get("/admin/")

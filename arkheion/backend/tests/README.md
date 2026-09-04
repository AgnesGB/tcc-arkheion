# Testes Unitários - Backend Arkheion

## Estrutura

A estrutura de testes foi organizada em módulos separados por funcionalidade:

```
backend/tests/
├── __init__.py
├── test_models_basicos.py    # Testes para Atributo, Pericia, Classe, Origem, Raça, etc.
└── test_models_ficha.py       # Testes para Ficha e models relacionados
```

## Módulos de Teste

### test_models_basicos.py

Testa os models fundamentais do sistema:

- **Atributo**: Força, Destreza, Constituição, Inteligência, Sabedoria, Carisma
- **Pericia**: Todas as perícias do sistema (Atletismo, Furtividade, etc.)
- **Classe**: Classes de personagem (Guerreiro, Mago, etc.)
- **Origem**: Origens dos personagens
- **Raca**: Raças disponíveis
- **Divindade**: Divindades do sistema
- **Habilidade**: Habilidades de classe, raça, origem, etc.
- **Ataque**: Ataques físicos e mágicos

### test_models_ficha.py

Testa o model Ficha (personagem do jogador) e relacionados:

- **Ficha**: Criação, cálculo de vida/mana, subir de nível
- **AtributoFicha**: Atributos específicos de uma ficha
- **PericiaTreinada**: Perícias treinadas, cálculo de valores, bônus de treino
- **NivelClasseFicha**: Níveis em classes (incluindo multiclasse)

**Testes importantes:**

- Cálculo de vida base + vida por nível
- Cálculo de mana para classes mágicas
- Sistema de treino de perícias por nível
- Perícias que requerem treino

## Executar os Testes

### Executar todos os testes

```bash
python manage.py test backend.tests
```

### Executar todos os testes com verbosidade

```bash
python manage.py test backend.tests -v 2
```

### Executar testes de um módulo específico

```bash
python manage.py test backend.tests.test_models_basicos
python manage.py test backend.tests.test_models_ficha
```

### Executar uma classe de teste específica

```bash
python manage.py test backend.tests.test_models_ficha.FichaModelTest
```

### Executar um teste específico

```bash
python manage.py test backend.tests.test_models_ficha.FichaModelTest.test_calcular_vida_com_classe
```

## Cobertura de Testes

Total de testes: **52 testes**

### Distribuição por módulo:

- **test_models_basicos.py**: 29 testes
- **test_models_ficha.py**: 23 testes

## Boas Práticas

1. **Isolamento**: Cada teste é independente e usa `setUp()` para configurar o ambiente
2. **Nomenclatura**: Nomes descritivos usando padrão `test_<ação>_<contexto>`
3. **Documentação**: Cada teste tem docstring explicando o que testa
4. **Organização**: Testes agrupados por model em classes TestCase
5. **Assertions**: Uso de assertions específicas do Django TestCase

## Testes de Serializers

Além dos testes de models, também há testes básicos para serializers:

```
backend/tests/
├── test_serializers_auth.py       # Testes para UserSerializer e autenticação
├── test_serializers_basicos.py    # Testes para serializers básicos
└── test_serializers_ficha.py      # Testes para FichaSerializer
```

### Executar testes de serializers

```bash
python manage.py test backend.tests.test_serializers_auth
python manage.py test backend.tests.test_serializers_basicos
python manage.py test backend.tests.test_serializers_ficha
```

# Documentação da API - ZSSN (Zombie Survival Social Network)

## Endpoints

### Registrar Sobrevivente

- **URL:** `/register-survivor/`
- **Método:** `POST`
- **Descrição:** Registra um novo sobrevivente junto com seu inventário.
- **Parâmetros:**
  - `name`: Nome do sobrevivente (string)
  - `age`: Idade do sobrevivente (int)
  - `gender`: Gênero do sobrevivente (string, 'male' ou 'female')
  - `last_location`: Última localização do sobrevivente (string, formato 'latitude,longitude')
  - `inventory`: Inventário do sobrevivente (objeto com `water`, `food`, `medication`, `ammunition`)

#### Exemplo de requisição:
```json
{
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "last_location": "35.6895,139.6917",
    "inventory": {
        "water": 10,
        "food": 5,
        "medication": 2,
        "ammunition": 50
    }
}
```
#### Respostas:
- ``201 Created`` em caso de sucesso.
- ``400 Bad Request`` se já existir um sobrevivente com o mesmo nome ou se os dados forem inválidos.`

### Obter Sobrevivente Atual
- **URL:** `/survivors/current/`
- **Método:** `GET`
- **Descrição:** Retorna o primeiro sobrevivente registrado.

#### Exemplo de resposta:
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 30,
  "gender": "male",
  "last_location": "35.6895,139.6917",
  "infected": false
}
```

### Obter Sobrevivente por Nome
- **URL:** `/survivors/get-by-name/`
- **Método:** `GET`
- **Descrição:** Retorna o sobrevivente e seu inventário pelo nome.
- **Parâmetros:**
  - `name`: Nome do sobrevivente (string)

#### Exemplo de resposta:
```json
{
  "survivor": {
    "id": 1,
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "last_location": "35.6895,139.6917",
    "infected": false
  },
  "inventory": {
    "water": 10,
    "food": 5,
    "medication": 2,
    "ammunition": 50
  }
}
```

### Reportar Infecção
- **URL:** `/report-infection/`
- **Método:** `POST`
- **Descrição:** Relata a infecção de um sobrevivente.
- **Parâmetros:**
  - `reporter_name`: Nome do sobrevivente que está relatando (string)
  - `reported_survivor_name`: Nome do sobrevivente que está sendo relatado (string)

#### Exemplo de requisição:
```json
{
  "reporter_name": "Jane Doe",
  "reported_survivor_name": "John Doe"
}
```
#### Respostas:
- ``200 OK`` se o sobrevivente for marcado como infectado.
- ``201 Created`` se a infecção for relatada mas o sobrevivente não for marcado como infectado.
- ``400 Bad Request`` se os dados forem inválidos.
- ``404 Not Found`` se o sobrevivente não for encontrado.

### Atualizar Localização do Sobrevivente
- **URL:** ``/api/survivors/<name>/update_location/``
- **Método:** ``PATCH``
- **Descrição**: Atualiza a última localização do sobrevivente.
- **Parâmetros:**
     - ``last_location``: Nova localização do sobrevivente (string, formato 'latitude,longitude')
    
#### Exemplo de requisição:
```json
{
  "last_location": "36.2048,138.2529"
}
```
#### Respostas:
- ``200 OK`` se a localização for atualizada com sucesso.
- ``404 Not Found`` se o sobrevivente não for encontrado.

### Marcar Sobrevivente como Infectado
- **URL:** ``/api/survivors/<name>/mark_infected/``
- **Método:** ``POST``
- **Descrição:** Marca um sobrevivente como infectado se ele receber 3 ou mais relatos de infecção.
- **Parâmetros:**
    - ``reporter_name``: Nome do sobrevivente que está relatando (string)
#### Exemplo de requisição:
```json
{
  "reporter_name": "Jane Doe"
}
```
### Respostas:
- ``200 OK`` se o sobrevivente for marcado como infectado.
- ``201 Created`` se a infecção for relatada mas o sobrevivente não for marcado como infectado.
- ``400 Bad Request`` se os dados forem inválidos.
- ``404 Not Found`` se o sobrevivente não for encontrado.
### Trocar Itens
- **URL:** ``/api/inventories/<survivor>/trade/``
- **Método:** ``POST``
- **Descrição:** Realiza a troca de itens entre dois sobreviventes.
- **Parâmetros:**
    - ``other_inventor``y: Nome do outro sobrevivente para troca (string)
    - ``offered_items``: Itens oferecidos pelo sobrevivente atual (objeto com water, food, medication, ammunition)
    - ``requested_items``: Itens solicitados do outro sobrevivente (objeto com water, food, medication, ammunition)
#### Exemplo de requisição:
```json
{
  "other_inventory": "Jane Doe",
  "offered_items": {
    "water": 5,
    "food": 2
  },
  "requested_items": {
    "medication": 1,
    "ammunition": 10
  }
}
```
#### Respostas:
- ``200 OK`` se a troca for realizada com sucesso.
- ``400 Bad Request`` se os dados forem inválidos ou se a troca não puder ser realizada.
### Relatórios
- **URL:** ``/reports/``
- **Método:** ``GET``
- **Descrição:** Retorna relatórios estatísticos sobre sobreviventes e inventários.
#### Exemplo de resposta:
```json
{
  "infected_percentage": 33.33,
  "uninfected_percentage": 66.67,
  "avg_water": 7.5,
  "avg_food": 3.5,
  "avg_medication": 1.0,
  "avg_ammunition": 25.0,
  "infected_points_lost": 250
}
```

## Vue Components

### DashboardPage
- **Descrição:** Página de dashboard que exibe informações sobre o sobrevivente atual e seu inventário.
- **Métodos:**
    - ``fetchSurvivorData()``: Busca os dados do sobrevivente atual.
- **Props:** Nenhum
- **Data:**
    - ``survivor``: Objeto com dados do sobrevivente
### HomePage
- **Descrição:** Página inicial com opções para login e registro de sobreviventes.
- **Props:** Nenhum

### LoginPage
- **Descrição:** Página de login para sobreviventes.
- **Métodos:**
    - ``login()``: Realiza o login do sobrevivente.
- **Data:**
    - ``survivorName``: Nome do sobrevivente (string)
### RegisterSurvivor
- **Descrição:** Página de registro de novos sobreviventes.
- **Métodos:**
    - ``registerSurvivor()``: Realiza o registro do sobrevivente.
    - ``checkMoreThanTen(itemType)``: Verifica se a quantidade de um item é maior que 10.
    - ``handleManualInput(itemType)``: Lida com a entrada manual de itens.
- **Data:**
    - ``name``: Nome do sobrevivente (string)
    - ``age``: Idade do sobrevivente (int)
    - ``gender``: Gênero do sobrevivente (string)
    - ``latitude``: Latitude da localização do sobrevivente (float)
    - ``longitude``: Longitude da localização do sobrevivente (float)
    - ``water``: Quantidade de água (int)
    - ``food``: Quantidade de comida (int)
    - ``medication``: Quantidade de medicação (int)
    - ``ammunition``: Quantidade de munição (int)
    - ``waterMore``: Entrada manual de água (int)
    - ``foodMore``: Entrada manual de comida (int)
    - ``medicationMore``: Entrada manual de medicação (int)
    - ``ammunitionMore``: Entrada manual de munição (int)
    - ``showManualInput``: Controle de exibição de entrada manual (objeto)

### ReportInfection
- **Descrição:** Página para reportar a infecção de um sobrevivente.
- **Métodos:**
    - ``reportInfection()``: Envia uma solicitação para reportar a infecção do sobrevivente.
    - ``goToDashboard()``: Navega de volta para o dashboard.
- **Data:**
    - ``reportedSurvivorName``: Nome do sobrevivente que será reportado como infectado (string)

### ReportsPage
- **Descrição:** Página que exibe relatórios estatísticos sobre os sobreviventes e seus recursos.
- **Métodos:**
    - ``created()``: Busca os relatórios ao carregar a página.
- **Data:**
    - ``reports``: Objeto contendo os dados dos relatórios.
### TradeItems
- **Descrição:** Página para troca de itens entre sobreviventes.
- **Métodos:**
    - ``getUserInventory()``: Busca o inventário do sobrevivente selecionado para troca.
    - ``loadUserInventory()``: Carrega o inventário do sobrevivente logado.
    - ``startTrade()``: Inicia o processo de troca de itens.
    - ``getMaxReceive(itemName)``: Obtém a quantidade máxima que pode ser recebida de um item.
    - ``getMaxSend(itemName)``: Obtém a quantidade máxima que pode ser enviada de um item.
    - ``sendTrade()``: Envia a solicitação de troca.
    - ``validateTrade()``: Valida os itens a serem trocados.
    - ``confirmTrade()``: Confirma a troca de itens.
    - ``goToDashboard()``: Navega de volta para o dashboard.
- **Data:**
    - ``username``: Nome do sobrevivente com quem será feita a troca (string).
    - ``userInventory``: Inventário do sobrevivente logado (objeto).
    - ``itemScores``: Pontuação dos itens (objeto).
    - ``selectedSurvivorInventory``: Inventário do sobrevivente selecionado (array).
    - ``selectedSurvivor``: Flag indicando se o sobrevivente foi selecionado (boolean).
    - ``showInventory``: Flag indicando se o inventário deve ser exibido (boolean).
    - ``tradeStarted``: Flag indicando se a troca foi iniciada (boolean).
    - ``tradeItems``: Lista de itens para troca (array).
    - ``itemTranslation``: Tradução dos nomes dos itens (objeto).
### UpdateLocation
- **Descrição:** Página para atualizar a localização do sobrevivente.
- **Métodos:**
    - ``updateLocation()``: Envia a solicitação para atualizar a localização do sobrevivente.
    - ``goToDashboard()``: Navega de volta para o dashboard.

## URLs
### URLs Principais
- ``/register-survivor/``: Endpoint para registrar novos sobreviventes.
- ``/survivors/current/``: Endpoint para obter o sobrevivente atual.
- ``/survivors/get-by-name/``: Endpoint para obter sobrevivente pelo nome.
- ``/report-infection/``: Endpoint para reportar infecção.
- ``/reports/``: Endpoint para obter relatórios estatísticos.
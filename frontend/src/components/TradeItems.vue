<template>
    <div class="container">
        <h1>Trocar Itens</h1>
        <div class="search-section">
            <label for="username">Nome do Sobrevivente:</label>
            <input type="text" id="username" v-model="username" required>
            <button @click="getUserInventory">Buscar Inventário</button>
        </div>
        <div class="grid">
            <div class="inventario_trade">
                <h2>Inventário do Sobrevivente Logado</h2>
                <h3>{{ $route.params.name }}</h3>
                <table class="styled-table">
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th>Quantidade</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Água</td>
                            <td>{{ userInventory.water }}</td>
                        </tr>
                        <tr>
                            <td>Comida</td>
                            <td>{{ userInventory.food }}</td>
                        </tr>
                        <tr>
                            <td>Medicação</td>
                            <td>{{ userInventory.medication }}</td>
                        </tr>
                        <tr>
                            <td>Munição</td>
                            <td>{{ userInventory.ammunition }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Botão de Iniciar Troca -->
            <div class="trade-button" v-if="showInventory && !tradeStarted">
                <button @click="startTrade">Iniciar Troca</button>
            </div>

            <!-- Tabela de Inputs para Troca -->
            <div v-if="tradeStarted" class="trade-inputs">
                <table class="styled-table">
                    <thead>
                        <tr>
                            <th>Enviar</th>
                            <th>Receber</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="items" v-for="item in tradeItems" :key="item.name">
                            <td>
                                {{ item.name }}: <input type="number" v-model.number="item.send" :max="getMaxSend(item.name)" min="0">
                            </td>
                            <td>
                                {{ item.name }}: <input type="number" v-model.number="item.receive" :max="getMaxReceive(item.name)" min="0">
                            </td>
                        </tr>
                    </tbody>
                </table>
                <button @click="confirmTrade">Confirmar Troca</button>
            </div>

            <div class="inventario_trade" v-if="showInventory">
                <h2>Inventário do Sobrevivente Selecionado</h2>
                <h3>{{ username }}</h3>
                <table class="styled-table" v-if="selectedSurvivor">
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th>Quantidade</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Água</td>
                            <td>{{ selectedSurvivorInventory.water }}</td>
                        </tr>
                        <tr>
                            <td>Comida</td>
                            <td>{{ selectedSurvivorInventory.food }}</td>
                        </tr>
                        <tr>
                            <td>Medicação</td>
                            <td>{{ selectedSurvivorInventory.medication }}</td>
                        </tr>
                        <tr>
                            <td>Munição</td>
                            <td>{{ selectedSurvivorInventory.ammunition }}</td>
                        </tr>
                    </tbody>
                </table>
                <div v-else>
                    <p>Inventário não encontrado para o sobrevivente selecionado.</p>
                </div>
            </div>
        </div>
        <h2>Tabela de Pontuação dos Itens</h2>
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Pontuação</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(score, item) in itemScores" :key="item">
                    <td>{{ item }}</td>
                    <td>{{ score }}</td>
                </tr>
            </tbody>
        </table>
        <button @click="goToDashboard">Voltar ao Dashboard</button>
    </div>
</template>

<script>


export default {
    name: 'TradeItems',
    data() {
        return {
            username: '',
            userInventory: {},
            itemScores: {
                Água: 4,
                Comida: 3,
                Medicação: 2,
                Munição: 1
            },
            selectedSurvivorInventory: [],
            selectedSurvivor: false,
            showInventory: false,
            tradeStarted: false,
            tradeItems: [
                { name: 'Água', send: 0, receive: 0 },
                { name: 'Comida', send: 0, receive: 0 },
                { name: 'Medicação', send: 0, receive: 0 },
                { name: 'Munição', send: 0, receive: 0 }
            ],
            itemTranslation: {
                'Água': 'water',
                'Comida': 'food',
                'Medicação': 'medication',
                'Munição': 'ammunition'
            }
        };
    },
    methods: {
        async getUserInventory() {
            const username = this.username;
            try {
                const response = await fetch(`http://localhost:8000/api/survivors/get-by-name/?name=${username}`);
                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('Sobrevivente infectado');
                    }
                    throw new Error('Sobrevivente não encontrado');
                }
                const data = await response.json();
                this.selectedSurvivor = data.survivor;
                if (this.selectedSurvivor.name === this.$route.params.name) {
                    throw new Error('Você não pode trocar itens com você mesmo');
                }
                this.selectedSurvivorInventory = data.inventory;
                this.showInventory = true;
                this.selectedSurvivor = true;
            } catch (error) {
                alert('Erro ao obter o inventário: ' + error.message);
            }
        },
        async loadUserInventory() {
            const username_trade = this.$route.params.name;
            try {
                const response = await fetch(`http://localhost:8000/api/survivors/get-by-name/?name=${username_trade}`);
                if (!response.ok) {
                    throw new Error('Erro ao carregar inventário do usuário');
                }
                const data = await response.json();
                this.userInventory = data.inventory;
            } catch (error) {
                alert('Erro ao carregar inventário do usuário: ' + error.message);
            }
        },
        startTrade() {
            this.tradeStarted = true;
        },
        getMaxReceive(itemName) {
            const translatedName = this.itemTranslation[itemName];
            return this.selectedSurvivorInventory[translatedName.toLowerCase()] || 0;
        },
        getMaxSend(itemName) {
            const translatedName = this.itemTranslation[itemName];
            return this.userInventory[translatedName.toLowerCase()] || 0;
        },
        async sendTrade() {
            try {
                const translateItemName = (item) => {
                    return this.itemTranslation[item.name] || item.name;
                };
                const username_trade = this.$route.params.name;
                const response = await fetch(`http://localhost:8000/api/api/inventories/${username_trade}/trade/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        other_inventory: this.username,
                        offered_items: this.tradeItems.map(item => ({ name: translateItemName(item), quantity: item.send })),
                        requested_items: this.tradeItems.map(item => ({ name: translateItemName(item), quantity: item.receive }))
                    })
                });

                const responseData = await response.json();
                
                if (response.ok) {
                    alert('Troca realizada com sucesso! ' + responseData.status);
                } else {
                    alert('Erro ao realizar troca: ' + responseData.error);
                }
            } catch (error) {
                alert('Erro ao realizar troca: ' + error.message);
            }
        },

        async validateTrade() {
            try {
                for (const item of this.tradeItems) {
                    const send = parseInt(item.send);
                    const receive = parseInt(item.receive);
                    if (isNaN(send) || isNaN(receive) || send < 0 || receive < 0) {
                        throw new Error('Os valores digitados devem ser números inteiros positivos');
                    }
                    if (send > this.getMaxSend(item.name) || receive > this.getMaxReceive(item.name)) {
                        throw new Error('Os valores digitados excedem a quantidade disponível');
                    }
                }
                if (this.tradeItems.every(item => item.send === 0 && item.receive === 0)) {
                    throw new Error('Nenhum item foi selecionado para troca');
                }
                if (this.tradeItems.every(item => item.send === 0) || this.tradeItems.every(item => item.receive === 0)) {
                    throw new Error('A troca deve ser feita de forma justa');
                }
                this.sendTrade();
                for (const item of this.tradeItems) {
                    item.send = 0;
                    item.receive = 0;
                }
                alert('Troca validada!');
            } catch (error) {
                alert('Erro ao validar a troca: ' + error.message);
            }
        },
        confirmTrade() {
            this.validateTrade();
        },
        goToDashboard() {
            this.$router.push(`/dashboard/${this.$route.params.name}`);
        }
    },
    mounted() {
        this.loadUserInventory();
    }
};
</script>

<style>
    .items {
        text-wrap: nowrap;
    }

    .items input {
        width: 50px;
    }

    .container {
        text-align: center;
    }

    .search-section {
        margin-bottom: 20px;
    }

    .grid {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        grid-gap: 20px;
        justify-content: center;
        align-items: center;
    }

    .inventario_trade {
        background-color: #3cb37257;
        margin: 0 auto;
        padding: 20px;
        border-radius: 5px;
    }

    .trade-button {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .trade-inputs {
        margin-top: 20px;
    }

    .styled-table {
        border-collapse: collapse;
        margin: 25px auto;
        font-size: 18px;
        border-radius: 5px 5px 0 0;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        width: 80%;
    }

    .styled-table thead tr {
        background-color: #009879;
        color: #ffffff;
    }

    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
    }

    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }

    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #009879;
    }

    .styled-table tbody tr.active-row {
        font-weight: bold;
        color: #009879;
    }

    button {
        padding: 10px 20px;
        font-size: 16px;
        background-color: #009879;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    button:hover {
        background-color: #007d65;
    }
</style>

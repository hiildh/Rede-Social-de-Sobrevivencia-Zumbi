<template>
    <div class="dashboard">
        <h1>Dashboard do Sobrevivente</h1>
        <div v-if="survivor">
            <div class="infos">
                <div class="profile">
                    <h2>Bem-vindo, {{ survivor.survivor.name }}</h2>
                    <p><strong>Idade:</strong> {{ survivor.survivor.age }}</p>
                    <p><strong>Gênero:</strong> {{ survivor.survivor.gender }}</p>
                    <p><strong>Última Localização:</strong> {{ survivor.survivor.last_location }}</p>
                </div>
                <div class="inventario">
                    <h3>Inventário</h3>
                    <ul class="inventario_li">
                        <li><strong>Água:</strong> {{ survivor.inventory.water }}</li>
                        <li><strong>Comida:</strong> {{ survivor.inventory.food }}</li>
                        <li><strong>Medicação:</strong> {{ survivor.inventory.medication }}</li>
                        <li><strong>Munição:</strong> {{ survivor.inventory.ammunition }}</li>
                    </ul>
                </div>
            </div>
            <div class="opcoes">
                <h3>Opções</h3>
                <ul class="submenu">
                    <li><router-link :to="`/update-location/${survivor.survivor.name}`">Atualizar Localização</router-link></li>
                    <li><router-link :to="`/report-infection/${survivor.survivor.name}`">Marcar como Infectado</router-link></li>
                    <li><router-link :to="`/trade-items/${survivor.survivor.name}`">Trocar Itens</router-link></li>
                    <li><router-link to="/reports">Relatórios</router-link></li>
                </ul>
            </div>
        </div>
        <div v-else>
            <p>Carregando...</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DashboardPage',
    data() {
        return {
            survivor: null
        };
    },
    created() {
        this.fetchSurvivorData();
    },
    methods: {
        async fetchSurvivorData() {
            const name = this.$route.params.name;
            try {
                const response = await fetch(`http://localhost:8000/api/survivors/get-by-name/?name=${name}`);
                if (response.ok) {
                    this.survivor = await response.json();
                    console.log(this.survivor);
                } else {
                    throw new Error('Erro ao buscar dados do sobrevivente');
                }
            } catch (error) {
                console.error('Erro ao buscar dados do sobrevivente:', error);
            }
        }
    }
};
</script>

<style>

.infos {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin-top: 20px;
}

.dashboard {
    text-align: center;
    padding: 50px;
}

.dashboard h1 {
    font-size: 2rem;
    margin-bottom: 20px;
}

.dashboard h2 {
    font-size: 1.5rem;
    margin-bottom: 10px;
}

.dashboard p,
.dashboard ul {
    font-size: 1.2rem;
    margin-bottom: 10px;
}

.profile {
    margin-top: 50px;
    background-color: #3cb37257;
    padding: 20px;
    border-radius: 5px;
}

.inventario {
    margin-top: 50px;
    background-color: #3cb37257;
    padding: 20px;
    border-radius: 5px;
}

.inventario_li {
    list-style: none;
    padding: 0;
}

.opcoes {
    margin-top: 50px;
    background-color: #3cb37257;
    padding: 20px;
    border-radius: 5px;
}

.submenu {
    list-style: none;
    padding: 0;
}

.submenu li {
    display: inline-block;
    margin: 10px;
}

.submenu a {
    padding: 10px 20px;
    background-color: #2e8b57;
    color: white;
    border-radius: 5px;
    text-decoration: none;
}

.submenu a:hover {
    background-color: #3cb371;
}
</style>

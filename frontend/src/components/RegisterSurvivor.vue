<template>
    <div class="register">
        <h1>Cadastro de Sobrevivente</h1>
        <form @submit.prevent="registerSurvivor">
            <fieldset>
                <legend>Dados Pessoais</legend>
                <div class="form-group">
                    <label for="name">Nome:</label>
                    <input type="text" id="name" v-model="name" required>
                </div>
                <div class="form-group">
                    <label for="age">Idade:</label>
                    <input type="number" id="age" v-model="age" required>
                </div>
                <div class="form-group">
                    <label for="gender">Sexo:</label>
                    <select id="gender" v-model="gender" required>
                        <option value="male">Masculino</option>
                        <option value="female">Feminino</option>
                    </select>
                </div>
            </fieldset>
            
            <fieldset>
                <legend>Localização</legend>
                <div class="form-group">
                    <label for="latitude">Latitude:</label>
                    <input type="number" step="any" id="latitude" v-model="latitude" required>
                </div>
                <div class="form-group">
                    <label for="longitude">Longitude:</label>
                    <input type="number" step="any" id="longitude" v-model="longitude" required>
                </div>
            </fieldset>

            <fieldset>
                <legend>Inventário</legend>
                <div class="inventory-grid">
                    <div class="form-group">
                        <label for="water">Água:</label>
                        <select id="water" v-model="water" required @change="checkMoreThanTen('water')">
                            <option value="0">Nenhum</option>
                            <option v-for="i in 10" :key="i" :value="i">{{ i }}</option>
                            <option value="more">Mais de 10</option>
                        </select>
                        <input v-if="showManualInput.water" type="number" v-model="waterMore" min="11" @blur="handleManualInput('water')" placeholder="Digite o número de águas">
                    </div>
                    <div class="form-group">
                        <label for="food">Alimentação:</label>
                        <select id="food" v-model="food" required @change="checkMoreThanTen('food')">
                            <option value="0">Nenhum</option>
                            <option v-for="i in 10" :key="i" :value="i">{{ i }}</option>
                            <option value="more">Mais de 10</option>
                        </select>
                        <input v-if="showManualInput.food" type="number" v-model="foodMore" min="11" @blur="handleManualInput('food')" placeholder="Digite o número de alimentos">
                    </div>
                    <div class="form-group">
                        <label for="medication">Medicação:</label>
                        <select id="medication" v-model="medication" required @change="checkMoreThanTen('medication')">
                            <option value="0">Nenhum</option>
                            <option v-for="i in 10" :key="i" :value="i">{{ i }}</option>
                            <option value="more">Mais de 10</option>
                        </select>
                        <input v-if="showManualInput.medication" type="number" v-model="medicationMore" min="11" @blur="handleManualInput('medication')" placeholder="Digite o número de medicamentos">
                    </div>
                    <div class="form-group">
                        <label for="ammunition">Munição:</label>
                        <select id="ammunition" v-model="ammunition" required @change="checkMoreThanTen('ammunition')">
                            <option value="0">Nenhum</option>
                            <option v-for="i in 10" :key="i" :value="i">{{ i }}</option>
                            <option value="more">Mais de 10</option>
                        </select>
                        <input v-if="showManualInput.ammunition" type="number" v-model="ammunitionMore" min="11" @blur="handleManualInput('ammunition')" placeholder="Digite o número de munições">
                    </div>
                </div>
            </fieldset>

            <button type="submit" class="btn">Cadastrar</button>
        </form>
    </div>
</template>

<script>
export default {
    name: 'RegisterSurvivor',
    data() {
        return {
            name: '',
            age: '',
            gender: '',
            latitude: '',
            longitude: '',
            water: 0,
            food: 0,
            medication: 0,
            ammunition: 0,
            waterMore: '',
            foodMore: '',
            medicationMore: '',
            ammunitionMore: '',
            showManualInput: {
                water: false,
                food: false,
                medication: false,
                ammunition: false
            }
        };
    },
    methods: {
        async registerSurvivor() {
            try {
                let foodValue = this.food;
                let waterValue = this.water;
                let medicationValue = this.medication;
                let ammunitionValue = this.ammunition;
                if (this.food === 'more') {
                    foodValue = this.foodMore;
                }
                if (this.water === 'more') {
                    waterValue = this.waterMore;
                }
                if (this.medication === 'more') {
                    medicationValue = this.medicationMore;
                }
                if (this.ammunition === 'more') {
                    ammunitionValue = this.ammunitionMore;
                }
                const water = parseInt(this.water);
                const food = parseInt(this.food);
                const medication = parseInt(this.medication);
                const ammunition = parseInt(this.ammunition);

                if (isNaN(waterValue) || isNaN(foodValue) || isNaN(medicationValue) || isNaN(ammunitionValue)) {
                    throw new Error('Os valores do inventário devem ser números válidos.');
                }

                const response = await fetch('http://localhost:8000/api/register-survivor/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: this.name,
                        age: this.age,
                        gender: this.gender,
                        last_location: `${this.latitude},${this.longitude}`,
                        inventory: {
                            water: waterValue,
                            food: foodValue,
                            medication: medicationValue,
                            ammunition: ammunitionValue
                        }
                    })
                });

                if (!response.ok) {
                    throw new Error('Erro ao cadastrar sobrevivente');
                }

                alert('Sobrevivente cadastrado com sucesso');
                this.$router.push('/');
            } catch (error) {
                alert('Erro: ' + error.message);
            }
        },

        checkMoreThanTen(itemType) {
            if (this[itemType] === 'more') {
                this[`${itemType}More`] = ''; 
                this.showManualInput[itemType] = true;
            } else {
                this.showManualInput[itemType] = false;
            }
        },
        handleManualInput(itemType) {
            if (parseInt(this[`${itemType}More`]) < 11) {
                this[itemType] = parseInt(this[`${itemType}More`]);
                this.showManualInput[itemType] = false;
            }
        }
    }
}
</script>

<style>
    .register {
        max-width: 700px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 10px;
        background: #fff;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    fieldset {
        margin-bottom: 20px;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    legend {
        padding: 0 10px;
        font-weight: bold;
        font-size: 1.2em;
    }
    .form-group {
        margin-bottom: 15px;
    }
    .form-group label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }
    .form-group input,
    .form-group select {
        width: 100%;
        padding: 8px;
        box-sizing: border-box;
    }
    .inventory-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 20px;
    }
    .btn {
        display: inline-block;
        padding: 10px 20px;
        background-color: #2e8b57;
        color: #fff;
        text-decoration: none;
        border-radius: 5px;
        cursor: pointer;
        border: none;
    }
    .btn:hover {
        background-color: #3cb371;
    }
</style>

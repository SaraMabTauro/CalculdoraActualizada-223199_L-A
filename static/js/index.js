function appendToExpression(value) {
    const input = document.getElementById('expression');
    
    // Lógica mejorada para manejar paréntesis
    if (value === '(' || value === ')') {
        // Lógica para validar paréntesis
        const currentValue = input.value;
        const openParens = (currentValue.match(/\(/g) || []).length;
        const closeParens = (currentValue.match(/\)/g) || []).length;

        if (value === '(') {
            // Permitir paréntesis de apertura libremente
            input.value += value;
        } else if (value === ')') {
            // Solo permitir cerrar si hay más paréntesis abiertos que cerrados
            if (openParens > closeParens) {
                input.value += value;
            }
        }
    } else {
        input.value += value;
    }
}

function clearExpression() {
    document.getElementById('expression').value = '';
    document.getElementById('token-list').innerHTML = '';
    document.getElementById('num-count').textContent = '0';
    document.getElementById('op-count').textContent = '0';
}

let memoryValue = null;

function appendToExpression(value) {
    document.getElementById('expression').value += value;
}

function clearExpression() {
    document.getElementById('expression').value = '';
    document.getElementById('token-list').innerHTML = '';
    document.getElementById('num-count').textContent = '0';
    document.getElementById('op-count').textContent = '0';
}

function backspace() {
    const input = document.getElementById('expression');
    input.value = input.value.slice(0, -1);
}

function memoryClear() {
    memoryValue = null;
}

function memoryStore() {
    const currentValue = document.getElementById('expression').value;
    if (currentValue && !isNaN(currentValue)) {
        memoryValue = currentValue;
    }
}

function memoryRecall() {
    if (memoryValue !== null) {
        document.getElementById('expression').value = memoryValue;
    }
}

function calculateTree() {
    const expression = document.getElementById('expression').value;
    fetch('http://127.0.0.1:5000/evaluate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expression })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('tree').innerHTML = data.treeHTML;
        document.getElementById('expression').value = data.result;
        updateTokenTable(data.tokens);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('tree').innerHTML = '<p>Error calculating expression</p>';
    });
}

function updateTokenTable(tokens) {
    const tokenList = document.getElementById('token-list');
    tokenList.innerHTML = '';
    
    let numCount = 0;
    let opCount = 0;

    tokens.forEach(token => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${token.value}</td>
            <td>${token.type}</td>
        `;
        tokenList.appendChild(row);

        if (token.type.includes('NUMERO')) numCount++;
        if (token.type.includes('OPERADOR')) opCount++;
    });

    document.getElementById('num-count').textContent = numCount;
    document.getElementById('op-count').textContent = opCount;
}
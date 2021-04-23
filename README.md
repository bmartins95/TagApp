# TAGApp

Implementação de um aplicativo para o gerenciamento e visualização de listas de TAG.

## Dependências

Para que o aplicativo possa ser executado as seguintes dependências serão necessárias:

- PyQt5 [5.15.2]
- sqlite3 [3.35.3]

Para evitar possíveis problemas, sugere-se utilizar as mesma versões citadas acima.

## Organização do código

Uma explicação geral da organização do código:

    .
    ├── figures          # Contém as figuras para ilustrar o readme
    ├── interface        # Janelas, menus, isto é, todas as estruturas da interface
    │   ├── menu         # Implementação da classe que cria a barra de menus
    │   └── shortcuts    # Implementação da barra de atalhos, e.g. ações e janelas de diálogo
    │       └── icons    # Icones dos atalhos
    └── server           # Interface com a sqlite3 e implementação do servidor

## Executando o aplicativo

Antes de executar o aplicativo rode o script **create_database.py** para adicionar alguns dados iniciais no banco de dados:

```python
python3 create_database.py
```

Para abrir o aplicativo execute o script **app.py**:

```python
python3 app.py
```

## Interface

### Descrição geral

A organização da interface segue as sugestões fornecidas no enunciado do teste. Sendo assim, os seguintes elementos estão presentes:

<p align="center">
    <img src="https://github.com/bmartins95/TagApp/blob/main/figures/interface.png">
</p>

1. Uma barra de menus com os menus "arquivo" e "ajuda". Dentro do menu "arquivo" temos os atalhos para "Criar projeto", "Abrir projeto", "Salvar projeto" e Fechar projeto. No menu "ajuda" o atalho "Sobre o app" pode ser utilizado para abrir uma janela com informações adicionais sobre o aplicativo.
2. Abaixo da barra de menus temos a barra de atalhos. Nesta barra as ações de "Abrir projeto", "Criar projeto", "Criar lista", "Salvar lista" e "Salvar todas as listas" podem ser executadas. Para que fique claro, a ação "Salvar lista" salva apenas a lista que está atualmente abertar na aba de listas.
3. Na esquerda temos uma interface de tipo "árvore" que contém os projetos abertos atualmente e as listas pertencentes a cada um destes projetos.
4. Na direita temos uma interface de abas que permite visualizar os valores dentro das listas.

### Abrir uma lista

Para abrir uma lista na aba de listas, pressione o botão esquerdo do mouse duas vezes sobre o nome dela na interface de projetos. Por exemplo, ao clicar duas vezes no nome "Lista 1", a tabela "Lista 1" pode ser visualizada na interface de abas.

<p align="center">
    <img src="https://github.com/bmartins95/TagApp/blob/main/figures/open_list.png">
</p>

### Alterar valores na lista

Para alterar valores na lista, pressione o botão esquerdo do mouse duas vezes sobre o valor que se deseja alterar. Por exemplo, ao clicar duas vezes, o valor na linha 5 da coluna de PID, i.e. "Falha", pode ser alterado.

<p align="center">
    <img src="https://github.com/bmartins95/TagApp/blob/main/figures/change_values.png">
</p>

### Adicionar linhas em uma lista

Para adicionar mais uma linha na lista, clique com o botão direito do mouse na aba que você deseja adicionar uma linha, em seguida, clique na opção "Adicionar linha".

<p align="center">
    <img src="https://github.com/bmartins95/TagApp/blob/main/figures/add_row.png">
</p>

### Fechar uma aba

Para fechar uma aba você pode pressionar o botão "x" ao lado do nome da aba, isto é:

<p align="center">
    <img src="https://github.com/bmartins95/TagApp/blob/main/figures/close_tab.png">
</p>

Qualquer alteração não salva na tabela será perdida ao fechar a sua aba. Futuramente deseja-se implementar uma funcionalidade que exibe um aviso quando o usuário tenta fechar uma aba com alterações não salvas. 
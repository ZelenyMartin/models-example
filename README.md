# Models Example

A small FastAPI server that returns a random literary work (prose, poetry or drama) as JSON on every request.

Your task is to write a **client** that downloads these works, **parses and validates** them into models, and **prints them nicely**. Watch out: some of the data the server returns is **valid** and some is **invalid**. Your client must tell them apart.

## Running the server

```bash
uv run fastapi dev main.py
```

The server runs at <http://127.0.0.1:8000>. Every `GET /` returns one random work:

```bash
curl http://127.0.0.1:8000/
```

The server loads the data from the [data/](data/) directory.

## Data format

Every work has these common fields:

| Field    | Type   | Rules                                    |
|----------|--------|------------------------------------------|
| `title`  | string | required, must not be empty              |
| `author` | string | required, must not be empty              |
| `genre`  | string | required, one of `prose`, `poetry`, `drama` |

What else a work contains depends on its `genre`.

### Prose (`genre: "prose"`)

- `text`: a non-empty string

```json
{
  "title": "Zlatovláska",
  "author": "Karel Jaromír Erben",
  "genre": "prose",
  "text": "Byl jeden král, a byl tak rozumný, ..."
}
```

### Poetry (`genre: "poetry"`)

- `poem`: a list of stanzas, where each stanza is a list of verses (non-empty strings)

```json
{
  "title": "Kytice",
  "author": "Karel Jaromír Erben",
  "genre": "poetry",
  "poem": [
    ["Zemřela matka a do hrobu dána,", "siroty po ní zůstaly;", "..."],
    ["I zželelo se matce milých dítek;", "duše její se vrátila", "..."]
  ]
}
```

### Drama (`genre: "drama"`)

- `text`: a list of lines. Each line is an object with **exactly one** key (the character's name), and the value is what they say (a non-empty string).

```json
{
  "title": "Naši furianti",
  "author": "Ladislav Stroupežnický",
  "genre": "drama",
  "text": [
    {"Bláha": "Dej pámbu dobrej večer, Josefe!"},
    {"Habršperk": "Dejž to pámbu, Valentýnku!"}
  ]
}
```

## Invalid data

Here are some ways the data can be invalid:

- a required field is missing (e.g. no `title` or `author`)
- a field is empty (`"title": ""`, `"text": ""`)
- a field has the wrong type (`"author": 42`, `"title": ["Název"]`)
- the `genre` doesn't match the content (e.g. `genre: "poetry"` on a drama)
- prose `text` is a list instead of a string
- poetry `poem` is a string instead of a list of stanzas
- a drama line is empty (`{}`), has more than one character, or has an empty or non-string value

## Task

1. Write a client that calls the server (`requests`).
2. Define models for `Prose`, `Poetry` and `Drama` and choose the correct one based on `genre`. You can do this in one of two ways:
   - **Manual validation:** write the checks yourself (`isinstance`, empty values, missing keys, ...). You will learn soon how tedious this can be.
   - **Pydantic:** use `pydantic` models and let Pydantic do the validation (types, constraints such as `min_length`, a discriminated union on `genre`, ...).
3. Validate the data. If it is invalid, print a clear error message and **don't crash**.
4. If it is valid, print the work nicely. For example:

```
Kytice
Karel Jaromír Erben
===================

    Zemřela matka a do hrobu dána,
    siroty po ní zůstaly;
    i přicházely každičkého rána
    a matičku svou hledaly.

    I zželelo se matce milých dítek;
    ...
```

```
Naši furianti
Ladislav Stroupežnický
======================

BLÁHA: Dej pámbu dobrej večer, Josefe!
HABRŠPERK: Dejž to pámbu, Valentýnku!
```

### Bonus

- Write tests for your models.

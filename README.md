# NetPinger

A Python library for querying game servers, inspired by GameDig. Currently supports:

- DayZ

## Installation 

```bash
pip3 install netpinger
```

## Usage

```python
from netpinger import query_server
```

<!-- P3fd3 -->
<!-- Pe9ea -->
<!-- P8050 -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NetPinger</title>
</head>
<body>
    <h1>NetPinger</h1>
    <p>A Python library for querying game servers, inspired by GameDig. Currently supports:</p>
    <ul>
        <li>DayZ</li>
    </ul>

    <h2>Installation</h2>
    <pre><code>pip3 install netpinger</code></pre>

    <h2>Usage</h2>
    <pre><code>from netpinger import query_server</code></pre>

    <h2>Badges</h2>
    <p>
        <img src="https://img.shields.io/pypi/v/netpinger" alt="PyPI version">
        <img src="https://img.shields.io/pypi/pyversions/netpinger" alt="Python versions">
        <img src="https://img.shields.io/github/license/wadedesign/netpinger" alt="License">
    </p>

    <h2>Example</h2>
    <p>Here is an example of how to use NetPinger to query a DayZ server:</p>
    <pre><code>import asyncio
from netpinger import query_server

async def main():
    result = await query_server("dayz", "172.111.51.154", 2303)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())</code></pre>

    <h2>Contributing</h2>
    <p>Contributions are welcome! Please open an issue or submit a pull request on GitHub.</p>

    <h2>License</h2>
    <p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>
</body>
</html>

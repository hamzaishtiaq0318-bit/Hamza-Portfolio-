import subprocess

script = """
setTimeout(() => {
    console.log('GLIDELY_HTML:' + document.body.innerHTML.slice(0, 1000));
}, 3000);
"""

# Let's run a test with CDP or playwright if available, or python script

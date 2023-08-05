# meeshkan-tutorial

An interactive tutorial for getting started with [Meeshkan](#what-is-meeshkan).

## Installation

Install via [pip](https://pip.pypa.io/en/stable/installing/):

```bash
$ pip install meeshkan-tutorial
```

This tutorial has been tested on Python 3.6, 3.7, and 3.8.

## Running

After installing, you can begin the tutorial by invoking from the command line:

```bash
$ meeshkan-tutorial
```

Once you've run this, you should see:

```bash
                             __    __
   ____ ___  ___  ___  _____/ /_  / /______ _____
  / __ `__ \/ _ \/ _ \/ ___/ __ \/ //_/ __ `/ __ \
 / / / / / /  __/  __(__  ) / / / ,< / /_/ / / / /
/_/ /_/ /_/\___/\___/____/_/ /_/_/|_|\__,_/_/ /_/


The tutorial!!
Press ENTER to continue...
```

If not, it's probably our fault. Please let us know on the [issues](https://github.com/meeshkan/meeshkan-tutorial/issues) page.

## What to expect

By the end of this tutorial, you'll know how to use Meeshkan to:
- Record server traffic from an API
- Transform those recordings into an OpenAPI spec
- Create a mock server from the spec

You'll repeat this two times: once to build a mock server that serves back recordings (similar to [wiremock](https://github.com/tomakehurst/wiremock) or [hoverfly](https://github.com/SpectoLabs/hoverfly)), and once to build a mock server that serves back synthetic data (similar to [unmock](https://github.com/meeshkan/unmock-js) or [fast-check](https://github.com/dubzzz/fast-check)).  The tutorial will end by showing how these two modes can be mixed.

## What is Meeshkan

[Meeshkan](https://github.com/meeshkan/meeshkan) is a tool for mocking HTTP APIs for use in sandboxes as well as for automated and exploratory testing. It uses a combination of API definitions, recorded traffic and code in order to make crafting mocks as enjoyable as possible.

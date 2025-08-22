# ExpyVR

_Copyright (©) 2009-2015 EPFL (Ecole Polytechnique fédérale de Lausanne)
Laboratory of Cognitive Neuroscience (LNCO)_

**ExpyVR** was originally inspired by psychopy but the execution pipeline was entirely redesigned to be based on OpenGL rendering. The code of ExpyVR is in Python, but it uses C/C++ shared libraries for multimedia I/O. It was developed for MS Windows (XP or 7) but the core engine is in itself non-OS specific (multi-platform Python modules).

**ExpyVR** allows users to easily design an experiment timeline with loops and randomization using a graphical user interface. Modules for 2D and 3D display, audio, or user input are integrated into the timeline with few clics. Once an experiment is described and saved, a set of execution instances can be generated with randomization for testing with subjects (e.g. factorial design).

## Design principles

1. Separation of the experiment design GUI and the experiment controller for execution

    GUI allows to design experiment as a set of modules instances + a flow with time-lines (XML)
    GUI generates instances (XML)
    Controller reads XML and executes instances

2. Components are developed and added easily

    Grouped by directories (default components, lncocomponents, etc.)
    Structure of a component is defined in OOP: fix set of methods (init, start, stop, clean), subclass of generic classes: basic, drawable, HUD, etc.
    Programming of components and scripting is done in Python

3. No external dependencies

    NO installation procedure for libraries (only for drivers if not possible otherwise)
    Runtime execution environment is provided with full set of dependencies

**ExpyVR** is provided as-is, with no support. A documentation is provided for learning to use and to develop new components. It is shared with the hope that it can be useful to researchers who, like us, need a high flexibility in the design and programming of their behavioral experiments.

## LICENSE

**ExpyVR** is free software ; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation ; either version 2 of the License, or (at your option) any later version.

**ExpyVR** is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY ; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ExpyVR ; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.

## Authors

Tobias Leugger

Bruno Herbelin bruno.herbelin@epfl.ch

Nathan Evans

Javier Bello Ruiz

Florian Lance


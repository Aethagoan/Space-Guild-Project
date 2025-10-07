<h1>WELCOME TO SPACE GUILD</h1>  
A space game--in a website.
<hr>
<h2>System Design Decisions</h2><br>
- Python over C#
<tab>C# is great. I love C#. But if you want to build complex handlers, such as something that can take in a string and give back a variety of differing object types? Talk about a nightmare. Python makes this really easy and makes my flow much more maintainable in this project. The tradeoff is how to manage packages ands separate code into different files, which is easier in C#.

- Dictionaries over Class Inheritance
<tab>At first, I thought that classes were the way to go. I wanted to define lots of classes that had complex inheritance and things, but when I realized that I could use sets and dictionaries for all* of my functionality in this project - Structures that are tried and tested and FAST - I never looked back.

- Redis over SQL
<tab>The main problem I researched was read-write speed for this project, because I wanted the ability for hundreds or even thousands of players to be able to login. You can't write that quickly to a regular database. 1000 requests every 5 seconds? Redis was the clear choice.

- 

<h2>Progress tracking:</h2>  
<ul>
<details>
    <summary><h3>Back End</h3></summary>
    <ul>
      <li>[ ] Ship statistics based on components? </li>
      <li>[X] Ship components</li>
      <li>[ ] Login System / token generation</li>
      <li>[ ] Logging <ul>
        <li>[ ] in region 'subscriber' pattern</li>
        <li>[ ] per ship log - messages and purely front-end added ship notifications (travel, damage, scanned, etc).</li>
        </ul>
      </li>
      <li>[ ] Station Shipyards/Vendor</li>
      <li>[ ] Anomalies (random events <s>at travel</s>)</li>
  </ul>
  </details>

  <details>
    <summary><h3>Front End</h3></summary>
    <ul>
      <li>[ ] Landing Page</li>
      <li>[ ] Login Page</li>
      <li>[ ] Game Page</li>
    </ul>
  </details>

  <details>
  <summary><h3>SOL SYSTEM</h3></summary>
    <ul>
      <li>[ ] POLITICS AND FACTION BUILDING</li>
      <li>[ ] Earth <ul>
        <li>[ ] Earth Orbit</li>
        <li>[ ] Earth Ground Station Zero</li>
        <li>[ ] Earth Orbital Station Zero</li>
        <li>[ ] Moon Orbit</li>
        <li>[ ] Moon Ground Station</li>
      </ul>
        <br>
      </li>
      <li>[ ] Sun Orbital</li>
        <br>
      <li>[ ] SOL -> ALPHA warp Gate orbital</li>
        <br>
      <li>[ ] Venus <ul>
        <li>[ ] Venus Orbit</li>
        <li>[ ] Venus Ground Station Zero</li>
        <li>[ ] Venus Orbital Station Zero</li>
      </ul>
        <br>
      </li>
      <li>[ ] Mars <ul>
        <li>[ ] Mars Orbit</li>
        <li>[ ] Mars Ground Station Zero</li>
        <li>[ ] Mars Orbital Station Zero</li>
        <li>[ ] Mars Moon 1 Ground Station</li>
        <li>[ ] Mars Moon 2 Ground Station</li>
       </ul>
      </li>
        <br>
      <li>[ ] Mercury <ul>
        <li>[ ] Mercury Orbit</li>
        <li>[ ] Mercury Ground Station</li>
       </ul>
      </li>
        <br>
      <li>[ ] Asteroid Belt <ul>
        <li>[ ] Belt Region 1 orbit <ul> 
          <li>[ ] Belt 1 Station</li>
        </ul>
        </li>
        <li>[ ] Belt Region 2 orbit <ul> 
          <li>[ ] Belt 2 Station</li>
        </ul>
        </li><li>[ ] Belt Region 3 orbit <ul> 
          <li>[ ] Belt 3 Station</li>
        </ul>
        </li>
       </ul>
      </li>
        <br>
      <li>[ ] Jupiter <ul>
        <li>[ ] Jupiter Orbit</li>
        <li>[ ] Jupiter Atmosphere Station 'Thunder Station'</li>
        <li>[ ] IO station</li>
       </ul>
      </li>   
        <br>
      <li>[ ] Saturn <ul>
        <li>[ ] Saturn Orbit</li>
        <li>[ ] Saturn Atmosphere Station 'Cloud Station'</li>
        <li>[ ] Ring station 1</li>
        <li>[ ] Ring station 2</li>
       </ul>
      </li>
        <br>
      <li>[ ] Uranus <ul>
        <li>[ ] Uranus Orbit</li>
        <li>[ ] Uranus Orbital Station</li>
        <li>[ ] Uranus Atmosphere station</li>
        </ul>
      </li>
        <br>
      <li>[ ] Kyper Regions <ul>
        <li>[ ] Kyper Region 1 Orbit + Station</li>
        <li>[ ] Kyper Region 2 Orbit + Station</li>
        <li>[ ] Kyper Region 3 Orbit + Station</li>
        <li>[ ] Kyper Region 4 Orbit + Station</li>
        </ul>
      </li>
      <li>[ ] built in code?</li> 
    </ul>
  </details>

  <details>
    <summary><h3>Seven more star systems</h3></summary>
    <ul>
      <li>[ ] Outer System 1 - <ul>
      <details>
        Science and research. <br> 
        **System composition in order inmost to outmost:**  <br>
        Binary star system.  <br>
        Close Gas Giant.  <br>
        Asteroid belt.  <br>
        Shattered planet w/ Orbital station and Deadly Ground Resource Gather site.  <br>
        Asteroid belt.  <br>
        Shattered planet w/ Oribital station and two Dangerous Ground Resource Gather sites.  <br>
        Synthetic planet w/ 2 Orbital stations and a Ground station.  <br>
        **Politics**  <br>
        A system of researchers using high-risk, high-reward scavengers to gather research materials from the shattered planets. All under the command of a few powerful barons trying to increase their wealth with SCIENCE!<br>
        **Warp Gate Connections:**<br>
        Synthetic planet orbital gates -> Nebula Gates  <br>
        Binary Star gates -> SOL  <br>
        Binary Star gates -> Black Hole  <br>
      </details>
        <li>[X] POLITICS AND FACTION BUILDING</li>
        <li>[X] gates?</li>
        <li>[X] planets</li>
        <li>[X] stations</li>
        <li>[ ] built in code?</li> 
        </ul>
      </li>
      <li>[ ] Outer System 2 - Empire<ul>
        <li>[ ] POLITICS AND FACTION BUILDING</li>
        <li>[ ] gates?</li>
        <li>[ ] planets</li>
        <li>[ ] stations</li>
        <li>[ ] built in code?</li> 
      </ul></li>
      <li>[ ] Outer System 3<ul>
        <li>[ ] POLITICS AND FACTION BUILDING</li>
        <li>[ ] gates?</li>
        <li>[ ] planets</li>
        <li>[ ] stations</li>
        <li>[ ] built in code?</li> 
      </ul></li>
      <li>[ ] Outer System 4<ul>
        <li>[ ] POLITICS AND FACTION BUILDING</li>
        <li>[ ] gates?</li>
        <li>[ ] planets</li>
        <li>[ ] stations</li>
        <li>[ ] built in code?</li> 
      </ul></li>
      <li>[ ] Outer System 5<ul>
        <li>[ ] POLITICS AND FACTION BUILDING</li>
        <li>[ ] gates?</li>
        <li>[ ] planets</li>
        <li>[ ] stations</li>
        <li>[ ] built in code?</li> 
      </ul></li>
      <li>[ ] Outer System 6<ul>
        <li>[ ] POLITICS AND FACTION BUILDING</li>
        <li>[ ] gates?</li>
        <li>[ ] planets</li>
        <li>[ ] stations</li>
        <li>[ ] built in code?</li> 
      </ul></li>
      <li>[ ] Outer System 7 - Zealots <ul>
        <li>[ ] POLITICS AND FACTION BUILDING</li>
        <li>[ ] gates?</li>
        <li>[ ] planets</li>
        <li>[ ] stations</li>
        <li>[ ] built in code?</li> 
      </ul></li>
    </ul>
  </details>
  <details>
    <summary><h3>The Nebula</h3></summary>
    <ul>
      <li>[ ] Gate/Teleporter/Warp orbit</li>
      <li>[ ] Storm Region</li>
      <li>[ ] Asteroid Fields</li>
      <li>[ ] Nebula Station 1</li>
      <li>[ ] Nebula Station 2</li>
      <li>[ ] built in code?</li> 
    </ul>
  </details>
  <details>
    <summary><h3>Black Hole</h3></summary>
    <ul>
      <li>[ ] Gate/Teleporter/Warp orbit</li>
      <li>[ ] Black Hole Orbit</li>
      <li>[ ] built in code?</li> 
    </ul>
  </details>
  <br>
</ul>


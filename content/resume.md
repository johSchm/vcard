<!--
  Resume cards, shown in this order.

  ## Title       starts a card
  when: / where: shown on the card (required)
  type:          extra gray tag next to the years, e.g. "Education" (optional)
  ### Title      an extra part inside the same card (e.g. a project or the thesis)
  when: / where: shown with the part (optional)

  Cards and parts can list their papers:
  papers:        keys from publications.bib (or PDF names), separated by commas. Each becomes a tag
                 like "ICML 2024" that jumps to the paper's card.

  Only used by the CV (tools/cv_pdf.py), not shown on the website:
  cv:            the short text for the CV. Without it the card or part is listed
                 with its title, place and years only. "cv: no" leaves it out.
  cv_section:    "Education" puts a card under Education, otherwise it is Experience.
                 On a part it lists that part as an entry of its own in that section.
-->

<!-- ## A Levels
when: 2007 - 2014
type: Education
where: Privatgymnasium Tangermünde, Germany

During this shaping period, my fascination with electrical circuits, programming and math emerged, igniting a passion that continues to fuel my academic and professional pursuits. -->

## Bachelor: Electrical Engineering
when: 2014 - 2018
where: Magdeburg-Stendal University of Applied Sciences, Germany
cv_section: Education
cv: Grade 1.7. Specialization in process automation. Thesis at ifak Magdeburg on a GUI for an ultrasonic sensor system on an embedded STM32 controller in C, grade 1.2.

I studied electrical engineering with a specialization in process automation. The program covered control theory, robotics, sensor technology, signal processing, and high- and low-voltage engineering. I programmed SIMATIC S7 PLCs, and microcontrollers in C, C++ and Assembler, including object-oriented programming. Much of the work was hands-on in the lab. Bringing circuits to life with software drew me to computer science.

### Internships and Student Jobs
when: 2013 - 2016
where: TCS AG Genthin, Bachmann GmbH Magdeburg, Enercon GmbH Magdeburg
cv: no

I first came into contact with the development and assembly of electrical circuit boards. I analyzed and evaluated wind turbine data and helped with the cabling of wind turbine control cabinets.

### Bachelor Thesis
when: 2017 - 2018
where: Institute for Automation and Communication (ifak) e.V. Magdeburg, Germany
cv: no

I developed a GUI in C for a clamp-on ultrasonic sensor system on an embedded controller, and analyzed and evaluated the overall measurement system.

## Master: Digital Engineering
when: 2018 - 2020
where: Otto von Guericke University Magdeburg, Germany
cv_section: Education
cv: Grade 1.4. Thesis at Fraunhofer IFF on vision-based human action recognition for human-machine interaction in industry, grade 1.1, published at ETFA 2021.

Coming from electrical engineering, I took advanced computer science courses and caught up on the foundations through self-study. Besides machine learning and data science, I learned databases and SQL, clean code, Git and continuous integration, and worked on robotics and robot swarms. Many courses were hands-on projects, some on my own and many in teams. I specialized in artificial intelligence, specifically deep learning.

### Master Thesis
when: 2019 - 2020
where: Fraunhofer Institute for Factory Operation and Automation IFF, Magdeburg, Germany
papers: Bexten2021
cv: no

I developed and integrated a vision-based deep learning model for real-time human action recognition, used for human-machine interaction in an industrial environment.

## Research Scientist at OVGU
when: 2020 - 2027
where: AILab, Otto von Guericke University Magdeburg, Germany
cv: Full-time position on funded R&D projects with industry partners, with the PhD pursued alongside.

Full-time position on funded R&D projects with industry partners. The projects set the topics, so my work spans several fields, from production scheduling to traffic signal control and acoustic sensing. I pursue my PhD alongside this work.

### SENECA
when: 2020 - 2022
where: with Thorsis Technologies GmbH and TECTRON GmbH
papers: Lang2021, Schmidt2021, Schmidt2024a
cv: Real-time production scheduling for the electronics manufacturer Tectron, NP-hard with up to 200 open orders per run. Methods published at ESWA, IFAC INCOM and HICSS. Delivered a planning tool with heuristic and deep learning methods to choose from, which beat manual planning on late orders and total tardiness in production. On 170 real orders, our simulated annealing method had no late orders and 23% fewer setups than a genetic algorithm, in 0.7 s instead of 66 s.

Real-time decision support for production scheduling at the electronics manufacturer Tectron, an NP-hard problem with up to 200 open orders per planning run. The methods of three papers come from this project (ESWA 2021, IFAC INCOM 2021 and HICSS 2024). We found that permutation-invariant networks trained on optimal schedules solve small instances but did not scale. At the end we handed Tectron a tool in which the planner chooses between heuristic and pure deep learning methods, including deep reinforcement learning and a genetic algorithm. In Tectron's production, it beat manual planning on late orders and total tardiness. On 170 real Tectron orders, the simulated annealing method from the project planned with no late orders, 23% fewer major setups and a 4.5% shorter makespan than a genetic algorithm, in 0.7 s instead of 66 s.

### AI-Engineering
when: 2022
where: joint project of five universities in Saxony-Anhalt
cv: New Bachelor's program in AI and engineering by five universities, running since 2023. Contributed to the curriculum and led the development of OERport, the cross-university course platform (Next.js, Shibboleth SSO, MySQL).

A new Bachelor's program that combines AI with engineering, built jointly by five universities. Students learn through team projects with regional companies and open course material instead of classic lectures. The program has been running since 2023. I contributed to the curriculum in the first project year. My main part was the platform. I led the development of OERport, the first platform that lets students and teachers share course material across the five universities. It runs on an Apache server, with a React/Next.js front end in Tailwind CSS, Shibboleth SAML single sign-on for all universities and a MySQL database of the course modules.

### Sustainable Supply Chain DeepHack
when: 2022
where: 2nd place, Transatlantic AI Hackathon
cv_section: Education
cv: Built in one weekend with a team: automatic parcel volume estimation with joint planning of vehicle loading and route.

In one weekend our team built a system that estimates the volume of parcels automatically and uses it to pack delivery vehicles more efficiently. The route is planned together with the loading order. Parcels are loaded first in, last out, so the next delivery is always within reach.

### PASCAL
when: 2022 - 2025
where: with Thorsis Technologies GmbH
papers: Schmidt2025a
cv: Traffic signal control on real-time V2X data for Magdeburg's urban testbed. Developed TransferLight with a Master's student I supervised, one reinforcement learning policy on a hierarchical graph neural network for any intersection layout. Trained only on synthetic networks, it left 54% fewer vehicles standing than fixed-time control at an unseen real intersection. Deployed the demonstrator as FastAPI services on two NVIDIA Jetson AGX Orin edge nodes, first rolled out in a SUMO simulation I largely wrote. Thorsis took it into practice after the project.

AI-based traffic signal control on real-time V2X data, built for Magdeburg's urban testbed. I developed the core component, TransferLight, with a Master's student I supervised. It is a single reinforcement learning policy on a hierarchical graph neural network that controls any intersection layout. Trained only on synthetic road networks, it transfers zero-shot to real ones (Cologne, Ingolstadt). It outperforms heuristic and learned baselines on travel time, waiting time and CO₂ emissions. On a real Cologne intersection it never saw in training, it left 54% fewer vehicles standing than fixed-time control and 16% fewer than MaxPressure.

I deployed the demonstrator on two NVIDIA Jetson AGX Orin 64GB edge devices, each a node in a multi-node server network. One node runs the traffic density regression, the other the signal phase prediction. Both serve their models through FastAPI with Uvicorn as the ASGI server. The demonstrator was first rolled out in a SUMO traffic simulation, which I wrote for the most part. After the project ended, Thorsis took it further into practice.

### KIVA-NET
when: 2025 - 2027
where: with Thorsis Technologies GmbH
cv: Low-cost acoustic sensor that counts and classifies vehicles from sound alone, in real time on edge hardware. Analytical signal processing pre-filters the audio, so only vehicle passes reach a frozen audio foundation model with a linear probe. 96.5% detection accuracy on more than 16,000 auto-labeled passes. Components from PASCAL and KIVA-NET are the basis of a multi-modal traffic sensor that Thorsis is developing.

Follow-up to PASCAL with the same industry partner. We are building a low-cost acoustic sensor that counts and classifies vehicles and rates traffic flow from sound alone, in real time on edge hardware. A video tracker labels the audio automatically and has labeled more than 16,000 vehicle passes so far.

The pipeline is heterogeneous on purpose. Cheap analytical signal processing finds the moments a vehicle passes and filters out the rest. Only these short windows reach a frozen audio foundation model, and a linear probe on its embeddings classifies them. This saves cost and time on the edge hardware and needs little training data. To size the model for the device, I benchmark foundation models and compact CNNs from 0.1 to 87 million parameters. our audio-based vehicle detection reaches 96.5% accuracy. Components from PASCAL and KIVA-NET are now the basis of a smart multi-modal sensor system for traffic monitoring that Thorsis is currently developing.

## PhD in Deep Learning at OVGU
when: 2022 - 2026
where: Otto von Guericke University Magdeburg, Germany
cv_section: Education
cv: Thesis research since 2022, alongside the full-time project work. Submission at the end of 2026; the PhD ends in April 2027.

Thesis research since 2022, alongside my full-time project work. It began with the work on radial beam sampling. I will submit the thesis at the end of 2026.

### OxML Summer School
when: August 2025
where: Oxford, United Kingdom

I attended the Oxford Machine Learning Summer School (OxML) on Representation Learning.

### PhD Thesis
where: AILab, Otto von Guericke University Magdeburg, Germany
cv: *Robust and Efficient Discriminative Deep Learning by Canonicalizing and Lifting Symmetry-Degenerated Signals.* A small module in front of a frozen pretrained model corrects the view of each input to ease the downstream task, which adds robustness across views. The methods act as preprocessing add-ons to frozen off-the-shelf models.

*Robust and Efficient Discriminative Deep Learning by Canonicalizing and Lifting Symmetry-Degenerated Signals.* A strong vision model can change its answer once the view of an object changes. My thesis develops canonicalization modules as a remedy. A small module in front of a frozen pretrained model undoes the transformation of each input, so robustness becomes an add-on that does not require retraining the downstream model. [Read the summary](#thesis).

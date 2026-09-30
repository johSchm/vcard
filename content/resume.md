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
cv: Grade 1.7. Thesis at ifak Magdeburg on a GUI for an ultrasonic sensor system on an embedded controller in C, grade 1.2.

While I enjoyed designing electrical circuits, I discovered my real passion in computer science. It gave me the power to bring those static circuits to life, and it still motivates me today.

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

I delved into advanced computer science courses, dedicating countless hours to self-study to bridge gaps in my knowledge. I truly found my passion when I dove into artificial intelligence, specifically deep learning.

### Master Thesis
when: 2019 - 2020
where: Fraunhofer Institute for Factory Operation and Automation IFF, Magdeburg, Germany
papers: Bexten2021
cv: no

I developed and integrated a vision-based deep learning model for real-time human action recognition, used for human-machine interaction in an industrial environment.

## Research Scientist at OVGU
when: 2020 - today
where: AILab, Otto von Guericke University Magdeburg, Germany
cv: Full-time position on funded R&D projects with industry partners, with the PhD pursued alongside. The projects set the topics, which is why my work spans several fields.

Full-time position on funded R&D projects with industry partners. These projects span a wide range of topics, from production scheduling to traffic signal control and acoustic sensing. This diversity has given me a broad knowledge base. I pursue my PhD alongside this work.

### SENECA
when: 2020 - 2022
where: BMBF-funded project with Thorsis Technologies GmbH and TECTRON GmbH
papers: Schmidt2021, Lang2021
cv: Real-time decision support for production scheduling at the electronics manufacturer Tectron, an NP-hard problem with up to 200 open orders per planning run. Developed deep learning approaches that find solution candidates with larger gains than existing heuristics. In Tectron's production, the final system beat manual planning on late orders and total tardiness.

Real-time decision support for production scheduling at the electronics manufacturer Tectron, an NP-hard problem with up to 200 open orders per planning run. I developed deep learning approaches that find solution candidates with larger gains than existing heuristics. Not everything worked: a permutation-invariant network trained on optimal schedules solved small instances but did not scale. The final system therefore lets the planner choose among several algorithms, including reinforcement learning and a genetic algorithm. In Tectron's production, it beat manual planning on late orders and total tardiness.

### AI-Engineering
when: 2022
where: BMBF-funded project of five universities in Saxony-Anhalt
cv: New Bachelor's program that combines AI with engineering, built by five universities and running since 2023. Contributed to the curriculum and led the development of the platform for sharing open educational resources across the universities.

A new Bachelor's program that combines AI with engineering, built jointly by five universities. I contributed to the curriculum in the first project year and led the development of the internal platform for open educational resources, which lets students and teachers share course material across the universities. Students learn through team projects with regional companies and open course material instead of classic lectures. The program has been running since 2023.

### Sustainable Supply Chain DeepHack
when: 2022
where: 2nd place, Transatlantic AI Hackathon
cv_section: Education
cv: Built in one weekend with a team: automatic parcel volume estimation with joint planning of vehicle loading and route.

In one weekend our team built a system that estimates the volume of parcels automatically and uses it to pack delivery vehicles more efficiently. The route is planned together with the loading order. Parcels are loaded first in, last out, so the next delivery is always within reach.

### PASCAL
when: 2022 - 2025
where: BMBF-funded project with Thorsis Technologies GmbH
papers: Schmidt2025a
cv: Traffic signal control on real-time V2X data for Magdeburg's urban testbed. Developed TransferLight together with a graduate student: a single reinforcement learning policy on a hierarchical graph neural network that controls any intersection layout and transfers zero-shot from synthetic to real road networks. It outperforms heuristic and learned baselines on travel time, waiting time and CO₂ emissions. Integrated with Thorsis into an operator-assistance prototype on edge hardware.

AI-based traffic signal control on real-time V2X data, built for Magdeburg's urban testbed. I developed the core component, a single reinforcement learning policy on a hierarchical graph neural network that controls any intersection layout. Trained only on synthetic road networks, it transfers zero-shot to real ones (Cologne, Ingolstadt). It outperforms heuristic and learned baselines on travel time, waiting time and CO₂ emissions. TransferLight was integrated with Thorsis into an operator-assistance prototype running on edge hardware.

### KIVA-NET
when: 2025 - 2027
where: ZIM-funded project with Thorsis Technologies GmbH
cv: Low-cost acoustic sensor that counts and classifies vehicles from sound alone, in real time on edge hardware. A video tracker labels the audio automatically. First models detect passing vehicles with 96.5% accuracy.

Follow-up to PASCAL with the same industry partner. We are building a low-cost acoustic sensor that counts and classifies vehicles and rates traffic flow from sound alone, in real time on edge hardware. A video tracker labels the audio automatically and has labeled more than 16,000 vehicle passes so far. On this data I benchmark models from compact CNNs to pretrained audio transformers to size the model for the edge device. First models detect passing vehicles with 96.5% accuracy.

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

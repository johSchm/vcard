<!--
  Service section (reviewing, supervision, ...). The text before the first ## is
  the introduction (optional). Cards are shown in the order of this file.

  ## Title     starts a card
  icon:        Font Awesome 5 icon classes, e.g. "fas fa-search" (required)
  when:        years, shown as a tag above the title (optional)

  "- Label: detail" lines in a card become rows with the label as a tag,
  e.g. "- ICLR 2027: 6 full papers".

  ### Title    adds a thesis to the card's list (sorted by date automatically, newest first)
  when:        date, e.g. "March 2026" (required)
  type:        "Master" or "Bachelor" (required)
  with:        company or institute the thesis was written with (optional)
  The text below is the abstract; it unfolds when the thesis is clicked (optional).
  Only title, date, partner and abstract are shown. The theses themselves and the
  students' names are not published.

  cv:          the card's line in the CV (tools/cv_pdf.py), not shown on the website.
               {reviewed} and {theses} are the counters below, {rows} the labels of the
               card's rows ("ICLR 2027, NeurIPS 2026, ..."). "cv: no" leaves the card out.

  For the counters in about.md:
  {reviewed} is the sum of the numbers in the rows of the "Reviewing" card,
  {theses} the number of ### theses in this file.
-->
Research depends on people who read, question and guide the work of others. This is my part in it.

## Reviewing
icon: fas fa-search
cv: {reviewed} papers for {rows}.

I review full and short papers for machine learning and computer vision conferences.

- ICLR 2027: 6 full papers
- NeurIPS 2026: 4 full papers
- ECCV 2026: 1 full paper
- ECCV: BISCUIT 2026: 3 full papers (workshop)
- NLDL 2026: 4 short papers

## Machine Learning Paper Club
when: 2022 - 2026
icon: fas fa-comments
cv: Initiated the machine learning paper club at OVGU and moderated it with colleagues, every two weeks from 2022 to 2026.

I initiated the paper club at Otto von Guericke University Magdeburg and moderated it together with colleagues. We met every two weeks to present and discuss recent papers in machine learning.

## Thesis Supervision
icon: fas fa-user-graduate
cv: {theses} Bachelor's and Master's theses, many with partners such as Fraunhofer IFF, Trumpf and SaxonQ. They led to two publications (AAAI workshop 2025, ECML-PKDD 2026).

I supervise Bachelor's and Master's theses at the AILab, many of them together with partners from industry and research institutes. The theses themselves are not public. Select a title to read its abstract.

### Ablation Study: Adaptation of YOLO11 for 3D Object Detection on Point Cloud Data
when: March 2026
type: Master
with: Fraunhofer IFF

This thesis is part of a bigger project that attempts to secure a fenceless robot cell according to human safety standards with LiDAR sensors and a connected object detection system. The focus of this thesis is on the object detection solution, which operates on point cloud data in 3D space and uses a derived YOLO model architecture for fast and accurate bounding box predictions. Besides preserving YOLO's inherently high inference speed, high detection recall and precision are of utmost importance for the industrial human safety application. Hence, this thesis conducts an ablation study on the adaptation of the state-of-the-art 2D object detector YOLO11 to generate reliable 3D detections for the project's use case. The ablation study evaluates the feasibility and impact of different strategies for various neural network components of the newly proposed YOLO3D11 framework. Finally, the overall goal of this thesis is the proposal of a fast, precise, and reliable neural network architecture that shows superior detection performance and overcomes the limitations of the baseline model, Complex-YOLOv4.

### Canonicalization-Based Adaptation of Pretrained Models to Affine Transformations via Out-of-Distribution Detection
when: December 2025
type: Master
with: University of Rostock

Many real-world classification tasks require invariance to specific transformations. Pretrained classifiers, however, are usually not trained on data exhibiting different transformations, leading to poor performance on transformed data. This thesis investigates the adaptation of models to achieve robustness against such transformations, specifically affine transformations, without additional training or fine-tuning on augmented data. Our approach builds on the idea of canonicalization, mapping transformed versions of the same image to a representative. If the network can categorize the representative, it can categorize the original data point. In our case the representative is chosen as the one minimizing an out-of-distribution (OOD) score. We show that the use of more general OOD detection methods that make use of earlier-layer features improves accuracy in comparison to previous methods using only the logits. This is done for several datasets including MNIST, EMNIST and SI-Score. In addition, we assess which search algorithms are suitable for finding the minima of continuous transformations. We show that choosing a search algorithm appropriate for a given budget can lead to higher accuracy. We compare against a supervised baseline that trains a classifier on augmented data, and a baseline model that is trained to distinguish between transformed and untransformed data while still using canonicalization. While canonicalization cannot match an augmented classifier in accuracy, it does not require the training or fine-tuning of a large model. When compared to an augmented model, canonicalization loses more accuracy on data that is not transformed. To address this, we examine whether the inlier score can be used to determine if the data is transformed, and only canonicalize data deemed to be out-of-distribution. We show that this can reduce the accuracy loss on untransformed data while still recovering most of the accuracy on transformed data compared to always canonicalizing. We also investigate whether this method is capable of detecting and correcting mispredicted transformations generated by regression-based approaches.

### Transformation-Invariant Neural Networks through Modulation
when: May 2025
type: Master

Convolutional Neural Networks (CNNs) have achieved remarkable success in computer vision tasks, yet they remain vulnerable to spatial transformations such as rotations and translations that are irrelevant to the semantic content of images. While data augmentation and architectural modifications like Spatial Transformer Networks have been proposed to address this limitation, they often require extensive retraining, introduce significant computational overhead, or fail to leverage the hierarchical representations already learned by pretrained models. This thesis presents a novel approach to achieving spatial transformation invariance through lightweight modulation modules that augment existing pretrained networks without modifying their core architecture. We thus introduce the Modulator, a recurrent neural network-based auxiliary module that operates alongside frozen pretrained models to provide input-conditional transformations. Unlike existing approaches that attempt to undo transformations in a single step or require complete architectural redesign, our method performs iterative, layer-wise corrections that progressively refine the feature representations. Our experimental evaluation on transformed versions of MNIST and FashionMNIST demonstrates significant improvements over baseline approaches. Our analysis also reveals that Modulators naturally learn to distribute transformations hierarchically, applying larger corrections at early layers where spatial information is abundant and minimal adjustments at deeper layers where representations are more abstract.

### Head and Gaze Controllable Implicit Motions
when: April 2025
type: Master
with: Casablanca.AI GmbH

Animating human heads with controllable head pose and gaze is a crucial task for applications in virtual avatars, video conferencing, and telepresence. In this thesis, we build upon the Implicit Motion Function (IMF) framework by introducing a novel pose-aware token architecture that enables fine-grained control over head and gaze direction while preserving expressions and identity. Our method includes a pose-aware token encoder that disentangles motion representations into three distinct tokens: pose, gaze, and expression-identity, derived from head pose and gaze vectors. These tokens guide a pose-aware decoder, which not only generates temporally coherent frames but also regresses head pose and gaze vectors to enforce alignment between control signals and visual output. To further enhance control over head motion, we propose an adversarial token disentanglement strategy that encourages separation of pose and expression features within the latent space. In addition, we introduce efficiency-oriented modifications to the IMF architecture, incorporating Linear Attention, PixelShuffle operations, and anti-aliasing techniques such as BlurPool-based downsampling and PixelShuffle upsampling. The proposed system is trained on the VoxCeleb1 dataset and demonstrates improved motion control, expression preservation, and computational efficiency. These contributions collectively extend the IMF framework with new capabilities, making it more expressive, controllable, and practical for real-world animation tasks.

### Employing Hand and Object Information for Human Action Recognition in Industrial Assembly Scenarios
when: September 2024
type: Master
with: Fraunhofer IFF

The field of Human Action Recognition is primarily focused on the analysis of extensive datasets containing a comprehensive range of human actions. However, actions that are particularly subtle and challenging to distinguish, such as those observed in industrial assembly scenarios, remain underexplored. This thesis presents an action recognition model and the corresponding data pipeline that address this research gap. To this end, a model that works on pre-extracted hand poses, object coordinates and tool coordinates was developed. These were transformed to heatmaps by adapting the methodology presented by Duan et al. (2022). These heatmaps were integrated into the common human action recognition model SlowFast by Feichtenhofer et al. (2018). On a custom-recorded dataset containing approximately 700 action instances of an example scenario, the developed method increased action recognition accuracy by 5.5% compared to the standard SlowFast model.

### Untersuchung von künstlichen neuronalen Netzen zur Detektion von Abweichungen in der Spurerkennung einer querführenden Fahrerassistenzfunktion
when: May 2024
type: Bachelor

Thanks to recent advances, automated and assisted driving has become one of the key future technologies in mobility. In this context, environmental perception through sensors plays a pivotal role in driver assistance functions. Typically, lane detection for lateral control is carried out using a camera. Deviations in lane recognition can lead to undesirable behavior. Therefore, it is important to detect anomalies in the lane data and deactivate the function in time if necessary. Due to the complexity of scenarios, rule-based approaches may reach their limits, making it advisable to deploy machine learning algorithms. Given their ability to learn patterns and relationships in data, they have great potential for application in error detection. This research aims to investigate the suitability of artificial neural networks for detecting deviations in lane recognition from the actual lane markings in the context of a lateral driver assistance function. First, a corresponding dataset is generated from test drives and processed. This is followed by the development of artificial neural networks, which will be trained, tested, and evaluated. The goal is to keep the scope of the procedure regarding storage capacity and runtime costs as low as possible to ensure suitability for real-time capability. Additionally, a rule-based algorithm is designed and tested. Finally, both methods are compared in terms of performance and critically assessed based on quality criteria and evaluation metrics. The results of the investigation show that the neural network is capable of effectively detecting lane recognition errors while achieving higher precision than the rule-based approach.

### Improving Interpolation in VAE using Riemannian Geometry
when: March 2024
type: Bachelor

### Domain Randomization of Deep Reinforcement Learning Environments for Zero-Shot Traffic Signal Control
when: December 2023
type: Master
with: Faculty of Mechanical Engineering, Otto von Guericke University Magdeburg

The escalating traffic demand in urban areas necessitates intelligent transportation engineering solutions that can regulate traffic more efficiently. The optimization of traffic signal control is considered a crucial factor in this regard. In recent years, deep reinforcement learning has gained traction as a potential solution concept to learn an adaptive signal controller, with promising initial results demonstrating its superiority over conventional solutions. However, the practical utility of such solutions is often constrained by a rigid model representation for the signal controller and a limited representation of traffic scenarios during the training phase. As a result, these methods severely overfit to the idiosyncrasies of the traffic environment used during training and fail to adapt to changing traffic conditions. To enhance adaptability, this thesis introduces TransferLight, a model architecture that employs neural message passing on a graph-structured state representation of an intersection to predict its next phase. This approach facilitates adaptability to arbitrarily structured intersections and is implemented for both a Q-learning and an advantage actor-critic algorithm. Additionally, a domain randomization mechanism is proposed, perturbing specific parameters associated with the road network and traffic within the environment during each training episode. This deliberate randomization aims to enhance the variability of traffic conditions encountered during the training phase. The efficacy of the proposed techniques is assessed by comparing them to established baseline solutions derived from conventional transportation engineering theories and reinforcement learning on both synthetically generated and real-world test scenarios. The findings reveal that TransferLight exhibits pronounced overfitting when trained on identical scenarios in each episode. Conversely, when the proposed domain randomization mechanism is leveraged to train TransferLight, generalization markedly improves and enables a zero-shot transfer to the test scenarios with a more consistent and robust performance, often being superior to the benchmark solutions, with respect to average travel time and throughput. However, upon closer examination within the context of an arterial road network scenario, the behavior of the trained model does not consistently align well with solutions specifically calibrated for this scenario. The latter exhibit improved signal progression, necessitating fewer stops for vehicles to traverse the arterial roadway. An estimation of model uncertainty using Monte Carlo dropout further indicates that despite the application of domain randomization during training, TransferLight's confidence in its predictions is not consistently high across traffic conditions, as the uncertainty distribution for some scenarios shows a noticeable shift or spread towards higher uncertainties. These observations imply that although the proposed domain randomization mechanism enhances the transfer performance of TransferLight to a wide range of traffic conditions, it does not implicitly equip the model with the necessary knowledge to act optimally and with a high degree of certainty on a consistent basis.

### Deep Reinforcement Learning for Universal Quantum Gates
when: October 2023
type: Master
with: SaxonQ

Quantum computers have the potential to lead to a paradigm shift in computing technology. However, while theoretical algorithms for quantum computers with which a range of computing problems previously deemed infeasible can be solved have been around for decades, their practical implementation is still an open problem. One of the main challenges in the construction of the required quantum computers is the implementation of universal, high-fidelity quantum gates. The controllability of quantum systems is limited by complex physical constraints which are difficult to overcome with classical methods. In recent years, Reinforcement Learning has gained increasing importance in quantum control and has been proven to be an effective tool in constrained environments. Additionally, due to the fault rates in current quantum computing technology, the length of feasible quantum circuits is limited. A quantum control method that is able to produce universal quantum gates with high fidelity would significantly shorten control circuits and make real-world applications more realistic. In this work, we apply a Dueling Double Deep Q-learning (DDDQL) approach to two quantum gate control tasks that are relevant for the development of universal quantum gates. We conduct our experiments in a restrictive environment with discretized control amplitudes and time steps for which we show that numerical control methods face difficulties. In the first task, we train DDDQL agents to generalize over changing physical environments. Our evaluation on the preparation of X and CNOT gates shows that this form of training leads to an overall more stable behavior. In the second task, we develop a training strategy based on curriculum learning that allows for DDDQL to generate control pulses for arbitrary single-qubit gates. We show that our learning strategy is able to produce control pulses that are adapted in length to a wide range of operations. We reach median fidelities above 0.999 for Rotational X gates and median fidelities above 0.99 for universal single-qubit gates. This shows that Deep Reinforcement Learning is able to produce high-fidelity control sequences for quantum gates and can generalize over a vast range of tasks. Therefore, on the road towards fault-tolerant universal quantum computing, Reinforcement Learning methods can be a crucial building block.

### Employing Neural Radiance Fields in Robotics
when: August 2023
type: Master
with: Fraunhofer IFF

One key factor for successfully using robotics to automate complex tasks is a capable perception system. While there are a multitude of methods for the perception of the geometry of a robot's surroundings, most of these perform poorly for glossy or transparent surfaces. This thesis examines whether employing neural radiance fields (NeRFs), a deep learning approach of generating an object model from posed RGB images, can be beneficial in these cases. It also investigates which modifications to the method might be useful when using NeRFs for robot perception. It concludes that NeRFs are better suited than traditional methods for recovering the geometric shape of challenging objects with non-Lambertian surfaces. The input encoding appears to be crucial for a good reconstruction quality with an anti-aliased, trainable encoding likely performing best. An advanced sampling scheme appears to be beneficial for the reduction of noise in the recovered geometry. Another finding of this thesis is that the quality of the data is essential for a successful reconstruction. The fidelity of the background removal and the accuracy of recovered camera parameters seem to be particularly impactful. Joint optimization of camera parameters is possible, but needs to be done carefully to ensure that the found values are physically sound. The best reconstruction quality can be reached with many training views, but depth supervision or a semantic consistency loss might help to increase the quality when few views are available. While the reconstruction results of NeRFs are impressive, an efficient implementation is deemed indispensable for making the method competitive in terms of computational cost when compared to traditional depth sensing approaches. It can be expected that future research will further improve the usefulness of NeRFs, simplifying their integration into a robotic system and rendering their use beneficial for many scenarios of robot perception.

### Solving Sequencing Problems Using Deep Reinforcement Learning
when: June 2023
type: Master
with: Trumpf

This master's thesis focuses on solving combinatorial optimization problems, specifically the Traveling Salesman Problem (TSP) with instances consisting of 10 and 20 cities, using the model-free A3C (Asynchronous Advantage Actor-Critic) algorithm implemented in the Ray framework. The research investigates the effectiveness of two different DRL agents: one with a pointer network as the actor and another with a transformer as the actor. The objective is to leverage the capabilities of DRL to predict optimal tours for the TSP and compare the results with known optimal tours. Combinatorial optimization problems pose computational challenges, requiring lengthy algorithms to be rerun for each new instance. By implementing the A3C algorithm on the Ray framework, the thesis explores the efficiency and scalability of the solution. The TSP is reformulated as a Markov decision process to enable the DRL agents to learn a meta-policy applicable to various TSP instances, eliminating the need for instance-specific policies. The implementation on Ray provides a distributed and scalable training environment, allowing for efficient utilization of computational resources. The performance of the proposed DRL agents is evaluated and compared against each other, as well as against existing DRL agents developed by Bello et al. The experimental results showcase the effectiveness of DRL in solving combinatorial optimization problems and highlight the advantages of leveraging the Ray framework for distributed and parallel training.

### Ampelsteuerung mit Graph Attention Networks und Deep Reinforcement Learning für Fahrzeitminimierung
when: May 2023
type: Bachelor
with: Faculty of Mechanical Engineering, Otto von Guericke University Magdeburg

Ongoing urbanization poses a variety of challenges to many areas of life. In particular, the growing traffic density in urban areas is a complex problem. Meeting this challenge requires advanced solutions that improve the efficiency of traffic flow and at the same time minimize environmental impact. Traffic lights are a central component of this optimization, as they directly influence traffic flow and road safety. This thesis presents an approach to traffic signal control based on Graph Attention Networks and Deep Reinforcement Learning. It evaluates whether such a model can realize a state-of-the-art traffic signal controller. In particular, it examines whether established methods such as Fixed Time or Max Pressure can be surpassed in control effectiveness. The main goal of the controller is to minimize the travel time of the individual vehicles. To evaluate the effectiveness of the model, several experiments were conducted that recreate different traffic scenarios such as nighttime or rush-hour traffic. The results show that, under the conditions set in this thesis, it was not possible to realize a more efficient traffic signal controller. For medium traffic volumes the controller is clearly less efficient than Fixed Time and Max Pressure. At extremely high traffic density it is about as effective as Max Pressure. For particularly low traffic volumes the model is entirely unsuitable. The literature suggests that implementing such systems is feasible in principle. (Translated from German.)

### Deep Reinforcement Learning-Based Proactive Traffic Light Control with Graph Neural Networks to Minimize CO2 Emissions
when: May 2023
type: Master
with: Faculty of Mechanical Engineering, Otto von Guericke University Magdeburg

Deep Reinforcement Learning (DRL) algorithms have recently been used extensively to create solutions for adaptive traffic signal control for reducing traffic congestion, improving travel time and improving throughput of intersections. Many of the methods are multi-agent reinforcement learning approaches which assign an agent to each intersection for effective traffic control. With these methods it becomes difficult to establish a cooperation between agents as the number increases. Some works also propose single-agent solutions which accept the entire environment as its state space, which again suffers from the problem of scalability when it comes to implementation to a large number of intersections. This thesis proposes a method which uses a single-agent solution with parameter sharing for all intersections, which is both scalable and generalizable over different kinds of intersections. The main objective is to explore whether these methods can minimize the CO2 emissions in a network of intersections without compromising on traffic flow as compared to some of the classical traffic control algorithms. Additionally, it suggests the use of Graph Neural Networks (GNN) along with the DRL methods to improve communication and interaction between neighboring intersections. The results show that DRL methods can successfully minimize CO2 emissions without compromising the traffic flow and also provide solutions that are scalable and generalizable and work on larger networks as well as intersections with different numbers of incoming lanes. The GNN-based DRL methods also work better than the classical traffic control algorithms for most of the scenarios and give a slight advantage in performance over the original DRL method. They outperform the DRL methods marginally in terms of minimizing the emissions. They work better in larger networks and can also generalize well over different types of intersections. The correlation between the traffic flow metrics and the emission also shows how improving traffic flows overall by reducing waiting time or the number of waiting vehicles leads to lower emissions.

### Proaktive Ampelschaltung mithilfe von Deep Multi-Agent Reinforcement Learning zur Fahrzeitminimierung
when: May 2023
type: Bachelor
with: Faculty of Mechanical Engineering, Otto von Guericke University Magdeburg

Urban traffic problems are a major challenge of the 21st century, manifesting in congestion, longer travel times and negative environmental effects. Intelligent transportation systems offer promising approaches to make traffic more efficient and to overcome these problems. This Bachelor's thesis investigates the proactive control of traffic lights with Deep Multi-Agent Reinforcement Learning to improve the efficiency of traffic flow and the adaptability of traffic signal control systems. The Multi-Agent Advantage Actor-Critic (MA2C) algorithm is presented and its performance is analyzed in different traffic scenarios, with particular attention to the effects of traffic volumes and traffic topologies. In addition, the influence of the MA2C algorithm on traffic-related emissions is examined. The results show that the MA2C algorithm is able to control traffic lights effectively and proactively, and that its application leads to a significant reduction in travel times and environmental impact. This thesis contributes to a deeper understanding of Deep Multi-Agent Reinforcement Learning in traffic control and points to new approaches for a more sustainable and efficient design of urban traffic systems. (Translated from German.)

### Sim-to-Real Transfer für eine mit Reinforcement-Learning programmierte Robotersteuerung
when: April 2023
type: Master

Reinforcement Learning has in recent years successfully been applied to many tasks. However, most development has been in simulated environments, which have the advantage of autonomously collecting samples faster than real time and avoid safety concerns. In domains such as robotics, a simulation is not sufficient due to unpredictable influences. The trained policies need to be applicable on a real robot as well, which leads to new problems, referred to as domain transfer. In this thesis, a robot controller is trained only in simulation. For the purpose of evaluation a Sim-to-Sim transfer is done, before testing it on a real robot. To improve the transfer, a combination of domain randomization and an improved simulation is used. It achieves a state-of-the-art success rate of 92.0 ± 5.3% on the transfer without any prior knowledge and no further training on the real robot.

### A Neural Network Performance Study: 3D Object Detection on Point Cloud Data for a Fenceless Robot Safety Application
when: March 2023
type: Bachelor
with: Fraunhofer IFF

This thesis is part of a bigger project that attempts to secure a fenceless robot cell according to human safety standards with LiDAR sensors and a connected object detection system. The focus of this thesis is on the object detection solution, which operates on 3D point cloud data and uses machine learning methods for fast and accurate bounding box predictions. This thesis investigates the state-of-the-art deep learning approaches to reliably detect objects in 3D point cloud data. Fast inference speeds as well as high detection and classification accuracy are of utmost importance for the industrial human safety application. Based on the project requirements the two best-suited neural networks are adapted to the project's use case and further improvements to their architecture are made. The resulting networks are evaluated on different data sets in order to deeply analyze their detection and classification performance with an emphasis on human safety. Finally, the overall goal of this thesis is the proposal of a fast and accurate neural network architecture that can be deployed in the project’s industrial human safety application for fenceless robot cells.

### Visualization and Evaluation of High-Dimensional Structures as Associations of Clusters in Subspaces
when: January 2023
type: Master

Visualizing, interpreting and clustering high-dimensional data is a challenging task in the field of information visualization. One major problem when clustering high-dimensional data is that it suffers from the curse of dimensionality, which means that in order to analyze high-dimensional data either an enormous amount of data is needed, or the dimensionality has to be reduced using dimension reduction techniques or subspace clustering. There have been many approaches that use different projection techniques in order to show high-dimensional data in two dimensions and use interaction methods such as zooming, dragging or transforming dimensions. For visualizing subspace clusterings, there have been different approaches that try to compare and visualize different subspaces or assess the quality of the subspace clustering results. In this thesis, I develop a new approach for visualizing cluster connections between different subspaces using the concept of association rules. A user interface is created in order to test the approach on different data sets and to change the parameters of the algorithm. In the end, I evaluate the stability of the approach and test its sensitivity to the curse of dimensionality.

### Forecasting Gasket Failures in H2 Refueling Stations Using Deep Multi-Task Learning
when: March 2022
type: Master
with: Dr. Ecklebe GmbH

In the current day and age, a popular alternative to Internal Combustion Engine Vehicles (ICEVs) is Electric Vehicles (EVs). While the former use internal combustion of a highly flammable liquid like gasoline or diesel to generate the rotational force required to turn the wheels of an automobile, the latter use electric motors for the same purpose. EVs can be categorized into two major subcategories: those that use a battery as a power source, called Battery Electric Vehicles (BEVs), and those that use a gas like H2 in combination with a fuel cell, called Fuel Cell Electric Vehicles (FCEVs). FCEVs are often referred to as environmentally neutral since the byproducts of an H2-powered automobile are water and oxygen. H2 is difficult to store in large amounts because it needs to be stored at high pressures, both at the fuel station and in the fuel tank of an automobile. These pressures range from 300 to 700 bar. With the advent of Industry 4.0, more and more manufacturers of H2 compressors use onboard intelligent systems to log data readings, which creates an inflow of sensor data. Many quantities, such as pressure and temperature readings at sealing gaskets and drive pressures during H2 compression, are logged constantly during the various phases of the refueling process and are used to monitor the running statistics of an H2 refueling system. Currently, such systems are monitored by humans to detect potential risk events in the near future, which is error-prone and often requires expert knowledge. This thesis models the current running state of a system to produce accurate near-future forecasts for one such component, and proposes a method to detect future anomalies that can be used to mitigate or detect risk events. Considering the inherent time-series nature of the logged data, the work proposes a novel approach for this preemptive warning solution. We model it as a multivariate, multi-step time-series forecasting problem, using a combination of Convolutional Neural Network (CNN) layers and Long Short-Term Memory (LSTM) cells to produce the forecasts in a regressive formulation. The risk-event detection is then formulated as a rule-based post-processing step involving expert knowledge, which is provided as a runtime-configurable parameter. Further, the forecasts are compared with naive statistical forecasting approaches like Exponential Smoothing. For the scope of this work, datasets from seven H2 refueling stations across Switzerland are considered. Furthermore, this thesis lays out the extraction, transformation and preprocessing of the sensor measurements from these compressors.

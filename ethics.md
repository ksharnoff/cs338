# Ethical Analysis of a Security Related Scenario

* Kezia Sharnoff
* October 15, 2025
* CS338 Computer Security


### (A) Identify the main ethical question or questions faced by the main character ("you") in the scenario. This will certainly include "what should you do?", but there may be other interesting questions to consider.

The main question is whether or not to report the bug to InstaToonz. Given InstaToonz history of going after previous bug reporters, this may come at a great personal cost to me. If I do decide to report it, I would need to figure out how to do this to make sure that they fix the bug and to avoid any legal consequences for me. 

### (B) For each stakeholder (or category of stakeholders) in the scenario, identify the stakeholder's relevant rights.

The InstaToonz company is a stakeholder with copy protection rights about the code and the secrecy of information. 

The board of trustees and investors of InstaToonz are stakeholders in this situation because they are financially tied to the success of InstaToonz. If InstaToonz has a public security mishap, for example if I go public with the bug or if a malicious actor steals all the messages, this would decrease the value of InstaToonz. 

I do not have many rights in this situation. If I am a genuine user of the InstaToonz app then I have a moral right to keep my messages secret. I maybe have a moral responsibility to help others as I am able to. Following section (j)(1) of the [DMCA](https://www.law.cornell.edu/uscode/text/17/1201), security testing is only permitted when the user is authorized from the owner or operator. Since I was not authorized, this security testing can be considered illegal. 

The users of InstaToonz have a moral right to privacy, that their private messages should stay secret. There could be many personal messages that would be bad if they were leaked. For example, the leaking of all the messages could help stalkers get information about their victims, out the sexuality or gender of someone, or breach lawyer-client confidentiality. 

### (C) List any information missing from the scenario that you would like to have to help you make better choices.

Another question is if the messages were encrypted. If the bug has to do with the implementation of the encryption, then I would be covered under section (g)(1) of the [DMCA](https://www.law.cornell.edu/uscode/text/17/1201) as I would be doing encryption research. If the encryption was implemented correctly but the key was not kept secret, then using it to view the unencrypted messages would be illegal under section [(a)(3)(A)]((https://www.law.cornell.edu/uscode/text/17/1201)). Therefore, more information about the bug would be helpful. 

More information about my background would also be helpful. If I am a current user of InstaToonz, then there may be some legitimacy of me finding and revealing this bug. More information about my job would be helpful as well, as the encryption research defense would only apply if I am in a "legitimate course of study, \[am\] employed, or \[am\] appropriately trained or experienced in the field of encryption technology" (g)(3)(B). 

### (D) Describe your possible actions, and discuss the likely consequences of those actions.

I could privately contact InstaToonz detailing the bug. They would likely try to figure out who I am, sue me, and report me to the FBI. The bug would likely get fixed. 

I could anonymously contact InstaToonz, detailing the bug. Perhaps I am a trained security professional and I do this in a way that they cannot tell who contacted them. They may fix the bug, or they may ignore it. They may still sue me if they can figure out who I am. 

I could reach out to a journalist who has an understanding of the stakes of this many accessible messages and have them (or their company) reach out to InstaToonz with the bug details and a time frame for when they will go public. InstaToonz will fix the bug but may also sue the news company. The news company could choose to go public with the information instead of contacting InstaToonz. 

I could reach out to a journalist or in some other way publicly publish the bug. InstaToonz would sue me and report me to the FBI, in addition, many private messages would be stolen and read. Publicly outing the bug without giving InstaToonz a chance to fix it would likely make it harder to argue in court about my security testing intentions. 

I could do nothing. I can consider that there is no way for me to anonymously contact InstaToonz and that I cannot deal with a lawsuit right now. This would mean the bug would stay an issue and a malicious actor may find it and leak all the messages. 

### (E) Discuss whether the ACM Code of Ethics and Professional Conduct offers any relevant guidance.

Section 1.2 emphasizes the importance of avoiding harm and section 1.1 mentions protecting an individual's right of autonomy. The direct messages of several hundred million people leaking would violate their autonomy and cause harm. Section 1.2 also says that: 

> a computing profession has an \[...\] obligation to report any signs of system risks that might result in harm \[...\] However, capricious or misguided reporting of risks can itself be harmful 

Following this code of ethics eliminates the options of not doing anything or publicly sharing the bug without first letting InstaToonz fix it. Both of those options would cause harm from the messages continuing being read or by guaranteeing that they will be leaked. 

### (F) Describe and justify your recommended action, as well as your answers to any other questions you presented in part A.

I think the potential downsides of leaving the bug are too vast: hundreds of millions of private messages being leaked could be a disaster. Therefore, I must notify InstaToonz about their bug. I will send anonymous messages to InstaToonz, describing their bug and detailing a timeline of a few months that they must fix the bug by or I will go public. This could be seen as a threat which InstaToonz may not like and could pursue legal action. I will send several (5-10) identical messages to the security and software engineering teams, in order to make sure that my message is received and dealt with accordingly. If I do not think I can disguise myself anonymously, I will use an intermediary cybersecurity journalist or other cybersecurity agency.
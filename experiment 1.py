#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from psychopy import data,event,visual,gui,logging ,core
import copy
import random

tp=0
stc=1
qst=2
asr=3
test_num=1

#Set diplay format for Japanese and Chinese
win=visual.Window(size=(1400,700),fullscr=False,screen=0,allowGUI=False,allowStencil=False,
                  monitor='testMonitor',color=[0,0,0],colorSpace='rgb',blendMode='avg',useFBO=True)
displayJP=visual.TextStim(win,font='MS Mincho',pos=(0,0),height=0.2,wrapWidth=1,ori=0,color='white',
                  colorSpace='rgb',opacity=1,depth=0.0)
displayCN=visual.TextStim(win,font=u'宋体',pos=(0,0),height=0.2,wrapWidth=1,ori=0,color='white',
                  colorSpace='rgb',opacity=1,depth=0.0)
displayCN1=visual.TextStim(win,font=u'宋体',pos=(0,0),height=0.089,wrapWidth=1,ori=0,color='white',
                  colorSpace='rgb',opacity=1,depth=0.0)                                 

def gen_trials(targets,fillers,rand_li):
    """
    Generate a trial list in which there are some filler sentence(s) between
    2 target sentences.
    
    Parameters
    ----------
    targets   : List
                List of information of each sentence that the research focuses
                on. 4 sorts of information are needed: 1) sentence type ; 2)
                sentence whose words are seperated by spaces; 3) question about
                the sentence; 4)answer of the question. eg.
                ('tt15a',u'野党の 議員が 支持した 官僚には 上流階級出身の 妻が いた。',u'野党の議員は官僚を支えましたか？','j')
            
               
    
    fillers   : List
                List of information of each sentence that is used to prevent 
                the subjects from recognizing the purpose of your experiment, 
                which may affect their performance. eg.
                ('f19',u'激しい 雨が 降ったので 試合は 中止した。',u'試合は雨のため中止でしたか？','j')
    
    rand_li   : List
                A randomly generated list whose elements indicate the positions
                of fillers and targets in the trial list
                
    Returns
    ----------
    trials    : List
                Trial list whose elements would be displayed one by one in the 
                experiment
    
    """
    trials=[]
    for num in rand_li:
        if num==0:
            trials.append(targets.pop())
        else:
            for j in range(num):
                trials.append(fillers.pop())
    return trials
    

def rand_trial(tgt_num,min_itv,max_itv):
    """
    Generate a list of number, which would be used to make sure that there
    are some filler sentence(s) between any 2 target sentences.
    
    Parameters
    ----------
    tgt_num: Int
             The number of target sentences
    
    min_itv: Int
             The minimum number of filler sentences between 2 target sentences
             max_itv >= 1.
             
    max_itv: Int
             The maximum number of filler sentences between 2 target sentences.
             Note that "tgt_num*max_itv <= the number of filler sentences".
             
    Returns
    ----------
    li     : List
             "li" contains 2 types of numbers, one is the number zero, the other
             is numbers that are greater than or equal to  one. Zero indicates
             a target sentence. Numbers greater than or equal to 0 indicate the 
             number of filler sentences between 2 targets. eg.
            
             "[2, 0, 1, 0, 1, 0, 2, 0, 2, 0]" would helps generating a trial 
             list in which 2 filler sentences is at the beginning of the trial
             list, then 1 target sentence, then 1 filler sentence, etc.
             
        
    
    """
    li=[]
    for i in range(tgt_num):
        #Randomly choose the interval between 2 target sentences
        rand_itv=random.randint(min_itv,max_itv)
        li.append(rand_itv)
        li.append(0)
    return li



def experiment(test_stc,trials):
    """
    Run an experiment.
    
    Paramenters
    ----------
    test_stc  : List
                A list of sentences displayed in pre-test.
    
    trials    : List
                A list of sentences displayed in formal test
    
    """
    #Record the information of the subject
    info={u'experiment':'exp1',u'name':'',u'level':[u'n1','not n1'],u'year':[u'三年生',u'四年生',u'四年生以上']}
    targetFile=open("%s.csv"%(info['experiment']+'_'+str(test_num)+'_'+info['level']+'_'+info['year']+'_'+info['name']+'_target'),'a')
    fillerFile=open("%s.csv"%(info['experiment']+'_'+str(test_num)+'_'+info['level']+'_'+info['year']+'_'+info['name']+'_filler'),'a')
    subject(info,targetFile,fillerFile) 
    displayCN1.setText(u'句子理解测试:\n  1.在接下来的测试中，屏幕将呈现被划分为几个'
                       u'片段的句子。每次屏幕上只呈现句子的\n一个片段，当确定自己能'
                       u'理解当前已呈现的内容时，可按下space空格键阅读下一个片段。'
                       u'2.当一个句子的所有片段呈现完毕时会出现有关该句子内容的问题'
                       u'回答是请按y,认为\n问题描述不正确或句子中未提及这样的内容请按n。'
                       u'\n  如无疑问，请按space空格键进入试测以熟悉规则。')
    displayCN1.draw()
    win.flip()
    #Run a pre-test
    test(test_stc,targetFile,fillerFile)
    displayCN.setText(u'按space空格键正式进入测试！')
    displayCN.draw()
    win.flip()    
    #Formal test
    test(trials,targetFile,fillerFile)
    #Save the data
    targetFile.close()
    fillerFile.close()
    thanks(u'感谢您对本次调查的支持与配合，\n祝您学习进步！')

def subject(info,targetFile,fillerFile):
    """
    Record the information of the subject.
    
    Paramenters
    ----------
    info      : Dictionary
                A dictionary in which information of the subject will be stored
    
    targetFile: file
                An excel file which will be used to  record the reading time and
                scores of the target sentences
                
    fillerFile: file
                An excel file which will be used to record the scores of the 
                filler sentences
    
    """
    gui.DlgFromDict(dictionary=info,title='personal information',order=[u'name',u'level',u'year',u'experiment'])
    targetFile.write('experiment,test,level,year,name\n'+info['experiment']+','+test_num+','+info['level']+','+info['year']+','+info['name']
                     +'\n\n type,RT,'+',,,,,,'+'point,response,answer\n')
    fillerFile.write('experiment,test,level,name\n'+info['experiment']+','+test_num+','+info['level']+','+info['year']+','+info['name']
                     +'\n\n type,point,response,answer\n')

def test(trials,targetFile,fillerFile):
    for trial in trials:
        stc_display(trial,targetFile,fillerFile)
        qst_display(trial)
        displayCN.setText(u'按space空格键进入下一个句子。')
        displayCN.draw()
        win.flip()
        
       
    
    
def stc_display(trial,targetFile,fillerFile):
    """
    Display a sentence to the subject and record the reading time of each word.
    
    """
    timer=core.Clock()  
    #Split the sentence into words
    sgmt_list=trial[stc].split()
    #Display the words one by one and record the reading time
    event.waitKeys(keyList=['space'])
    for sgmt in sgmt_list:
        display(displayJP,sgmt,0.0)
        timer.reset()
        event.waitKeys(keyList=['space'])
        timeUsed=timer.getTime()
        #If the sentence is a target sentence, then its reading time should be 
        #recorded.
        if 'tt' in trial[tp]:
           targetFile.write(trial[tp]+','+str(timeUsed)+',')
        if 'f' in trial[tp]:
           fillerFile.write(trial[tp]+',') 
                
def qst_display(trial,targetFile,fillerFile):
    """
    Display the question of a sentence to the subject and record the answer
    and score.
    
    """
    #Display the question of the sentence 
    display(displayJP,u'***問題***',1.0)
    displayJP.setText(trial[qst])
    displayJP.draw()
    win.flip()
    #Get the answer and record the score
    key_li=event.waitKeys(keyList=['f','j'])
    for key in key_li:
        if(key==trial[asr]):
            point=1
        else:
            point=0
            display(displayJP,u'正しくないよ',2.0)
    if 'tt' in trial:
       targetFile.write(str(point)+','+key+','+trial[asr]+'\n')
    if 'f' in trial[tp]:
       fillerFile.write(str(point)+','+key+','+trial[asr]+'\n')
       

def thanks(sentence):
    """
    Say thankyou to the subject and close the display window.
    
    Parameters
    ----------
    sentence  : String
                A sentence that expresses your appreciation to the subject
    
    """
    display(displayCN,sentence,5.0)
    win.close()
    
def display(form,text,t):
    """
    Display text in a particular format for some time.
    
    Parameters:
    ----------
    form      :   The format in which text is displayed
    
    text      :   String
                  Text to be displayed
    
    t         :   Float
                  "t" specifies the time for which the text would be dispalyed
                  
    """
    form.setText(text)
    display.draw()
    win.flip()
    core.wait(t)


from pyrouge import Rouge155


def get_rouge(model):
    r = Rouge155('/home/lyn/ROUGE/ROUGE-1.5.5/RELEASE-1.5.5/')
    r.system_dir = '/home/lyn/liuwei/Summary_Server/summaryserver/systems/'
    r.model_dir = '/home/lyn/liuwei/Summary_Server/summaryserver/' + model + '/'
    r.system_filename_pattern = 'system.(\d+).txt'
    r.model_filename_pattern = 'model.#ID#.txt'
    output = r.convert_and_evaluate()
    output_dict = r.output_to_dict(output)
    return output_dict

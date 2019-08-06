require 'csv'
require 'time'

all_data = CSV.read('./2018_contest_result.csv')
students = CSV.read('./studentlist.csv')
contests = CSV.read('./contestlist.csv')

$flag = [[false, false, false],
        [false, false, false],
        [false, false, false],
        [false, false, false],
        [false, false, false],
        [false, false, false]
       ]


def initialize_flag
  $flag = [
    [false, false, false],[false, false, false],[false, false, false],
    [false, false, false],[false, false, false],[false, false, false],
  ]
  return $flag
end

def check_problem(problem)
  case problem
  when "Q01" then x = 0
  when "Q02" then x = 1
  when "Q03" then x = 2
  when "Q04" then x = 3
  when "Q05" then x = 4
  when "Q06" then x = 5  
  end
  return x
end

def check_contest(contest)
  flag = false
  case contest
    when "W09_C01" then flag = true
    when "W10_C01" then flag = true
  end
  return flag
end

def check_flag_T01(problem)
  score = 0
  x = check_problem(problem)
  if $flag[x][0] == false
    $flag[x][0] = true
    score += 50
  end
  return score
end

def check_flag_T02(problem)
  score = 0
  x = check_problem(problem)
  if $flag[x][1] == false
    if $flag[x][0] == false
      $flag[x][0] = true
      score += 50
    end
    $flag[x][1] = true
    score += 50
  end
  return score
end

def check_flag_T00(problem, time, decrease_t, base_score, contest)
  score = 0
  x = check_problem(problem)
  check_contest(contest)
  if $flag[x][2] == false
    if $flag[x][1] == false
      $flag[x][1] = true
      if (base_score > 100) || (check_contest(contest) && x >= 4)
        score += 50
      end
      if $flag[x][0] == false
        $flag[x][0] = true
          score += 50
      end
    end
    
    $flag[x][2] = true                                                                                                                                                                                    
    if time < decrease_t
      score += 50 + 30
    elsif time < 60
      early_time = ((60-time)/5).to_i
      score += 50 + ( early_time + 1) * 5
    else
      score += 50
    end
  end                                                                                                                                                                                                    
  return score                                                                                                                                                                                           
end

contests.each do |contest|
  base = Time.parse(contest[1])
  students.each do |student|
    sum = 0
    previous = base

    $flag = initialize_flag()
    each_csv = CSV.generate do |csv|
      csv << ["past_time_from_start", "past_time_from_prev", "problem_num","test_num", "user_id", "score", "submit_time"]
      csv << [0, 0, 'Q00', 'T00',student[0], 0, 0]

      all_data.each do |data|
        if ( data[4] == student[0] && data[2] == contest[0])
          diff_from_start = (Time.parse(data[7]) - base)/60
          diff_from_prev = (Time.parse(data[7]) - previous) / 60
          
          if ( data[5] == "T01")
            score = check_flag_T01(data[3])
          elsif(data[5] == "T02")
            score = check_flag_T02(data[3])
          elsif(data[5] == "T00")
            score = check_flag_T00(data[3], diff_from_start, contest[2].to_i, contest[5].to_i, contest[0])
          end

          if ( diff_from_start >= 180)
            next
          end
          if score == 0
            next
          end
          sum += score
          each_csv = [
            diff_from_start,
            diff_from_prev,
            data[3],
            data[5],
            data[4],
            sum,
            data[7]
          ]
          previous = (Time.parse(data[7]))
          csv << each_csv
        end
      end
    end
    puts each_csv

    File.open("./"+contest[0]+"/"+student[0]+".csv", "w") do |file|
      file << each_csv
    end

  end
end

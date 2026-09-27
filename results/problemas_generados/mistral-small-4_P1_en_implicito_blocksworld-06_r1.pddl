(define (problem blocksworld-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (ontable b)
    (clear f)
    (on e b)
    (on f e)
    (ontable c)
    (clear d)
    (on a c)
    (on d a)
    (handempty)
  )
  (:goal (and
    (on c b)
    (on b a)
    (on a e)
    (on e f)
    (on f d)
  ))
)

(define (problem blocksworld-problem)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (ontable b)
    (on e b)
    (on f e)
    (clear f)
    (ontable c)
    (on a c)
    (on d a)
    (clear d)
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

(define (problem blocksworld-problem)
  (:domain blocks)
  (:objects
    a b c d e f - block
  )
  (:init
    (clear f)
    (clear d)
    (handempty)
    (on f e)
    (on e b)
    (ontable b)
    (on d a)
    (on a c)
    (ontable c)
  )
  (:goal (and
    (on c b)
    (on b a)
    (on a e)
    (on e f)
    (on f d)
  ))
)
